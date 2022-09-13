import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later

from .models import *
# from .views import consumerView

class ChatConsumer(AsyncWebsocketConsumer):


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

  # Receive message from WebSocket
    # async def adminStart(self, text_data):
    #     print('adminStart triggered')

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        value = data.get('value')
        playerID = data.get('player_id')
        admin = data.get('admin')
        print('receiving from websocket')
        # if (admin == 'admin'):
        #     print('message received!!')
        #     # def consumerView(game_id, player_id):
        #     print('consumerView engaged!')
        #     # Stores the name of all the players
        #     player_names = []
        #     # Number of players in game
        #     players = Player.objects.filter(game=game_id)
        #     # Obtain the game instance
        #     game_instance = Game.objects.get(id=game_id)
        #     # Game instance has started and is no longer waiting for players 
        #     game_instance.is_game_waiting = False
        #     # Game is running
        #     game_instance.is_game_running = True
        #     game_instance.save()
            
        #     # Checks for number of players before assigning teams
        #     if len(players) >= 4:
        #         # Calculating the amount of teams and distributions
        #         # number of players/4 players per team and +1 to round number
        #         number_of_teams = int(players.count()/4)
        #     elif len(players) > 0 and len(players) < 4:
        #         # Single team
        #         number_of_teams = 1
        #     else:
        #         pass

        #     print("***************************************************************")
        #     print(" This is a print for Teams algorithm confirmation only for debugging")
        #     print("game = " +str(game_instance.id))
        #     print("players = "+str(len(players)))
        #     print("teams =" +str(number_of_teams))
        #     print("teammates = " +str(int(len(players)/number_of_teams)))
        #     print("***************************************************************")

        #     # All player names assignation,
        #     for player in players:
        #         # appends the players name
        #         player_names.append(player.username)
            
        #     ########### this can improve into the same random_name function. TBD ##########
        #     # empty list that will store all the team names
        #     team_names=[]
        #     # appends the team names based on the number of teams
        #     for i in range(0,number_of_teams):
        #         # assigns a random name to name
        #         name = random_name()
        #         # appends the names and removes the suffix \n from the raw file
        #         # team_names.append(name.removesuffix("\n"))
        #         team_names.append(name)
        #     ##########

        #     # Dictionary with the sorted teams
        #     teams = get_teams(team_names, player_names)
        #     print("***************************************************************")
        #     print(team_names)
        #     print(teams)
        #     print("***************************************************************")
        # ############################## Works fine in here ########################################
        #     # List comprehension
        #     for teamName, teamMember in teams.items():
        #         # Creating new team
        #         new_team, created_flag = Team.objects.get_or_create(name=teamName, game=game_instance)
                
        #         # # Search for the players names inside the team
        #         for participant in teamMember:
        #             # Gets the player based on the name and is assigned to team assignation
        #             team_assignation = Player.objects.get(username=participant)
        #             # Assigns the team to the player model
        #             team_assignation.team = new_team
        #             team_assignation.save()
        #         #     game_id = game_instance.id
        #         #     player_id = player.id
        #         #     teams_id = new_team.id

        #     team_id = new_team.id
        #     game_id = game_instance.id
        #     player_id=player_id
        #     team_players= Player.objects.filter(team=new_team)
        #     # consumerView(room, playerID)
        # print(value)
        

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
    
    