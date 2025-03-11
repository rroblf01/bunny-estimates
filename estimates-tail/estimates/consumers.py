import asyncio
import json
import logging
import uuid

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from estimates.models import Room, Vote

logger = logging.getLogger(__name__)


class RoomConsumer(AsyncWebsocketConsumer):
    users = {}
    actual_topic = None
    timeout_task = 5
    room_info = {}
    topic_info = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_public_name"]
        self.room_group_name = f"room_{self.room_name}"
        try:
            self.room = await Room.objects.aget(public_name=self.room_name)
        except Room.DoesNotExist:
            await self.close(code=4004)
            return

        if self.room_group_name not in self.room_info:
            self.room_info[self.room_group_name] = {}

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notify other users about the disconnection
        await self.generic_notify("user_disconnected", {"user_id": self.user_id})

        # If the disconnecting user is the leader, transfer leadership
        if self.room_info[self.room_group_name][self.user_id].get("is_leader"):
            await self.transfer_leadership()

        del self.room_info[self.room_group_name][self.user_id]

        if not self.room_info[self.room_group_name]:
            del self.room_info[self.room_group_name]

    async def get_topics(self, data):
        topics = []
        async for topic in (
            self.room.topic_set.select_related("task").all().order_by("id")
        ):
            topics.append(
                {
                    "id": topic.id,
                    "title": topic.task.title,
                    "description": topic.task.description,
                    "average": await topic.average_votes,
                }
            )
        self.topic_info[self.room_group_name] = next(
            (topic["id"] for topic in topics if not topic["average"]), None
        )
        return {
            "room_name": self.room.name,
            "topics": topics,
            "actual_topic": self.topic_info[self.room_group_name],
        }

    def _generate_id(self):
        return str(uuid.uuid4())

    def _get_user_list(self):
        return [
            {
                "user_id": k,
                "name": v.get("name"),
                "vote": v.get("vote"),
                "is_leader": v.get("is_leader"),
            }
            for k, v in self.room_info[self.room_group_name].items()
        ]

    async def add_user(self, data):
        user_id = self._generate_id()
        user_data = {"user_id": user_id, "name": f"User {user_id.split('-')[0]}"}
        await Vote.objects.aget_or_create(
            topic_id=self.topic_info[self.room_group_name],
            voter_external_id=user_id,
            voter_name=user_data["name"],
        )

        await self.generic_notify("user_added", {"user": user_data})
        user_to_return = user_data.copy()
        user_to_return.update({"participants": self._get_user_list()})
        self.room_info[self.room_group_name][user_id] = user_data

        # Store the user_id in the instance
        self.user_id = user_id

        # Assign the first user as the leader
        if not any(
            user.get("is_leader")
            for user in self.room_info[self.room_group_name].values()
        ):
            self.room_info[self.room_group_name][user_id]["is_leader"] = True
            user_to_return["is_leader"] = True
            await self.generic_notify("leader_assigned", {"user_id": user_id})

        return user_to_return

    async def user_added(self, event):
        user = event["user"]
        # Aquí puedes definir lo que quieres hacer cuando se añade un usuario
        await self.send(text_data=json.dumps({"type": "user_added", "user": user}))

    async def vote(self, data):
        user_id = data["user_id"]
        value = data["vote"]

        # Update the user's vote
        if user_id in self.room_info[self.room_group_name]:
            self.room_info[self.room_group_name][user_id]["vote"] = value
            vote = await Vote.objects.aget(
                topic_id=self.topic_info[self.room_group_name],
                voter_external_id=user_id,
            )
            vote.point = value
            await vote.asave()

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

    async def rename(self, data):
        user_id = data["user_id"]
        name = data["name"]

        # Update the user's name
        if user_id in self.room_info[self.room_group_name]:
            self.room_info[self.room_group_name][user_id]["name"] = name
            vote = await Vote.objects.aget(
                topic_id=self.topic_info[self.room_group_name],
                voter_external_id=user_id,
            )
            vote.voter_name = name
            await vote.asave()

        # Notify other users about the name change
        await self.generic_notify("user_renamed", {"user_id": user_id, "name": name})

    async def user_renamed(self, event):
        user_id = event["user_id"]
        name = event["name"]
        # Aquí puedes definir lo que quieres hacer cuando se cambia el nombre de un usuario
        await self.send(
            text_data=json.dumps(
                {"type": "user_renamed", "user_id": user_id, "name": name}
            )
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

    async def transfer_leadership(self):
        # Transfer leadership to another user if the leader leaves
        if self.room_info[self.room_group_name]:
            new_leader_id = next(
                (
                    user_id
                    for user_id, user in self.room_info[self.room_group_name].items()
                    if not user.get("is_leader")
                ),
                next(iter(self.room_info[self.room_group_name])),
            )
            self.room_info[self.room_group_name][new_leader_id]["is_leader"] = True
            await self.generic_notify("leader_assigned", {"user_id": new_leader_id})

    async def assign_leader(self, data):
        current_leader_id = data["user_id"]
        new_leader_id = data["new_leader_id"]
        if (
            new_leader_id in self.room_info[self.room_group_name]
            and current_leader_id in self.room_info[self.room_group_name]
            and self.room_info[self.room_group_name][current_leader_id].get("is_leader")
        ):
            # Remove current leader status
            for user in self.room_info[self.room_group_name].values():
                user["is_leader"] = False
            # Assign new leader
            self.room_info[self.room_group_name][new_leader_id]["is_leader"] = True
            await self.generic_notify("leader_assigned", {"user_id": new_leader_id})

    async def leader_assigned(self, event):
        user_id = event["user_id"]
        await self.send(
            text_data=json.dumps({"type": "leader_assigned", "user_id": user_id})
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["action"]

        get_data_to_response = {
            "get_topics": self.get_topics,
            "add_user": self.add_user,
            "vote": self.vote,
            "rename": self.rename,
            "assign_leader": self.assign_leader,
            "start_round": self.handle_start_round,
        }

        method = get_data_to_response.get(message, lambda: None)
        data_to_return = await method(text_data_json)
        if data_to_return:
            data_to_return.update({"type": message})
            await self.send(text_data=json.dumps(data_to_return))

    async def handle_start_round(self, data):
        # Notify all members of the room that the round has started
        await self.generic_notify("start_round", {"seconds": self.timeout_task})

        # Start the countdown in a separate task
        asyncio.create_task(self.end_round_after_delay(self.timeout_task))

    async def end_round_after_delay(self, delay):
        # Wait for the specified delay
        await asyncio.sleep(delay)

        for user in self.room_info[self.room_group_name].values():
            user["vote"] = None

        # Notify all members of the room that the round has ended
        topic = await self.room.topic_set.aget(id=self.topic_info[self.room_group_name])
        task = await sync_to_async(lambda: topic.task)()
        task.completed = True
        await task.asave()

        avegare = await topic.average_votes

        self.topic_info[self.room_group_name] = None
        async for topic in self.room.topic_set.all():
            if not await topic.average_votes:
                self.topic_info[self.room_group_name] = topic.id
                break

        # Create news Votes
        if self.topic_info[self.room_group_name]:
            for user_id in self.room_info[self.room_group_name].keys():
                await Vote.objects.acreate(
                    topic_id=self.topic_info[self.room_group_name],
                    voter_external_id=user_id,
                    voter_name=self.room_info[self.room_group_name][user_id]["name"],
                )

            await self.generic_notify(
                "end_round",
                {
                    "average": avegare,
                    "next_topic_id": self.topic_info[self.room_group_name],
                },
            )

    async def start_round(self, event):
        seconds = event["seconds"]
        await self.send(
            text_data=json.dumps({"type": "start_round", "seconds": seconds})
        )

    async def end_round(self, event):
        average = event["average"]
        topic_id = event["next_topic_id"]
        await self.send(
            text_data=json.dumps(
                {"type": "end_round", "average": average, "next_topic_id": topic_id}
            )
        )

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
