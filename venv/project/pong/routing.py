from django.urls import re_path
from . import consumer_pong
from . import consumer_match

websocket_urlpatterns = [
	re_path(r'ws/pong/game$', consumer_pong.ConsumerMatch.as_asgi()),
    re_path(r'ws/pong$', consumer_pong.ConsumerPong.as_asgi()),
]