from django.urls import re_path

from estimates.consumers import RoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/room/(?P<room_name>\w+)/$", RoomConsumer.as_asgi()),
]
