import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("room name")
        self.room_group_name = 'chat_%s' % self.room_name
        

    # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # username = event['username']
        # self.send(text_data=json.dumps({
        #     'username': username
        # }))

    async def disconnect(self, close_code):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'disc',
                'message': "remove player",
                'username': 'userName',
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name          
        )
        print('consumer disconnect')

    # async def websocket_disconnect(self, message):
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         { 'type': 'dc_message' }
    #     )
    #     await super().websocket_disconnect(message)

  # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        # value = data.get('value')
        # print(value)
        print('receiving from websocket')

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
# Receive message from room group
    async def disc(self, event):
        print('disc')
        message = event['message']
        username = event['username']
        value = event.get('value')

    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'value' : value,
        }))

# Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        value = event.get('value')
        print('receiving from room group')

    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'value' : value,
        }))
    
    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)