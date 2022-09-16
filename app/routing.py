from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()), # Using asgi
  path('ws/game_session/<int:room_name>', consumers.ChatConsumer.as_asgi()),
  path('ws/team_session/<int:room_name>', consumers.ChatConsumer.as_asgi()),
]