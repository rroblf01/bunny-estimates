import json
import logging
import stat

from channels.generic.websocket import WebsocketConsumer

from estimates.models import Room

logger = logging.getLogger(__name__)


class RoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_public_name"]
        try:
            self.room = Room.objects.get(public_name=self.room_name)
        except Room.DoesNotExist:
            self.close(code=4004)
            return
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        logger.info(f"Received message {message}")
        self.send(
            text_data=json.dumps({"message": message, "room_name": self.room_name})
        )
