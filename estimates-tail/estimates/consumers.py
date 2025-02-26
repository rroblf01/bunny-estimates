import json
import logging
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer

from estimates.models import Room

logger = logging.getLogger(__name__)


class RoomConsumer(AsyncWebsocketConsumer):
    users = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_public_name"]
        self.room_group_name = f"room_{self.room_name}"
        try:
            self.room = await Room.objects.aget(public_name=self.room_name)
        except Room.DoesNotExist:
            await self.close(code=4004)
            return
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify other users about the disconnection
        await self.generic_notify("user_disconnected", {"user_id": self.user_id})

    async def get_topics(self, data):
        topics = []
        async for topic in self.room.topic_set.select_related("task").all():
            topics.append(
                {
                    "id": topic.id,
                    "title": topic.task.title,
                    "description": topic.task.description,
                    "average": await topic.average_votes,
                }
            )
        actual_topic = next(
            (topic["id"] for topic in topics if topic["average"]), topics[0]["id"]
        )
        return {
            "room_name": self.room.name,
            "topics": topics,
            "actual_topic": actual_topic,
        }

    def _generate_id(self):
        return str(uuid.uuid4())

    def _get_user_list(self):
        return [
            {"user_id": k, "name": v.get("name"), "vote": v.get("vote")}
            for k, v in self.users.items()
        ]

    async def add_user(self, data):
        user_id = self._generate_id()
        user_data = {"user_id": user_id, "name": f"User {user_id.split('-')[0]}"}
        await self.generic_notify("user_added", {"user": user_data})
        user_to_return = user_data.copy()
        user_to_return.update({"participants": self._get_user_list()})
        self.users[user_id] = user_data

        # Store the user_id in the instance
        self.user_id = user_id

        return user_to_return

    async def user_added(self, event):
        user = event["user"]
        # Aquí puedes definir lo que quieres hacer cuando se añade un usuario
        await self.send(text_data=json.dumps({"type": "user_added", "user": user}))

    async def vote(self, data):
        user_id = data["user_id"]
        value = data["vote"]

        # Update the user's vote
        if user_id in self.users:
            self.users[user_id]["vote"] = value

        # Notify other users about the vote
        await self.generic_notify("user_voted", {"user_id": user_id, "vote": value})

    async def generic_notify(self, event_type, data={}):
        notification = {"type": event_type, **data}
        await self.channel_layer.group_send(self.room_group_name, notification)

    async def user_disconnected(self, event):
        user_id = event["user_id"]
        # Aquí puedes definir lo que quieres hacer cuando se desconecta un usuario
        await self.send(
            text_data=json.dumps({"type": "user_disconnected", "user_id": user_id})
        )

    async def user_voted(self, event):
        user_id = event["user_id"]
        vote = event["vote"]
        # Aquí puedes definir lo que quieres hacer cuando un usuario vota
        await self.send(
            text_data=json.dumps(
                {"type": "user_voted", "user_id": user_id, "vote": vote}
            )
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["action"]

        get_data_to_response = {
            "get_topics": self.get_topics,
            "add_user": self.add_user,
            "vote": self.vote,
        }

        method = get_data_to_response.get(message, lambda: None)
        data_to_return = await method(text_data_json)
        if data_to_return:
            data_to_return.update({"type": message})
            await self.send(text_data=json.dumps(data_to_return))

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
