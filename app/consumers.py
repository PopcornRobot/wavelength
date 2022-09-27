import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async, async_to_sync # Implement later

from .models import *
from .views import clue_form

class WavelengthConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("connecting to room")
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

    # async def adminStart(self, text_data):
    #     print('adminStart triggered')
  
  # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        username = data.get('username')
        game = data.get('game')
        value = data.get('value')
        playerID = data.get('player_id')
        admin = data.get('admin')
        clue = data.get('clue')
        action = data.get('action')
        team = data.get('team')
        question = data.get('question')
        # print('text data should be here:' + text_data)
        # print(data)
        if (action == 'submit clue'):
            await self.create_gameturn(data)

        print('receiving from websocket')    
        
        # await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': message,
                'username': username
            }        
        )
        print('sending message to room group')
    
    @sync_to_async
    def create_gameturn(self, data):
        print('clue form engaged!')
        clue_form(data)  

# Receive message from room group
    async def disc(self, event):
        print('disc')
        message = event.get('message')
        username = event.get('username')
        value = event.get('value')

    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'value' : value,
        }))

# Receive message from room group
    async def broadcast(self, event):
        message = event.get('message')
        username = event.get('username')
        value = event.get('value')
        print('receiving from room group')

    # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'value' : value,
        }))
    
    # @sync_to_async
    # def save_message(self, username, room, message):
    #     Message.objects.create(username=username, room=room, content=message)
    
    