from unicodedata import name
from unittest import expectedFailure
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from .models import *
import random

teams_placeholder = {}

def index(request):
    
    return render(request, 'app/index.html')

def room(request, room_name):
    username= request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]

    context = {'room_name' : room_name, 'username' : username, 'messages' : messages}
    return render(request, 'app/room.html', context)

# This function opens a file that stores a list of 250 team names and resturns a random name from the list
def random_name():
    # open the file
    with open("app/static/txt/team_names.csv") as f:
        # Assigns all the lines
        name_list = f.readlines()
        # Random assignation of a single name from the list
        new_name = name_list[random.randint(0,len(name_list))]
    # Returns a new randome name
    return new_name

# When a player wants to play he/she has to type a username and select start/join.
# creating the player objects
# When a player wants to play the game selects "Start Game" or "Join game"
# the player is redirected to this function where the game objects are created
def game_registration(request, game_id):
    if request.GET == 'GET':
        # Assigns the form input to the players name
        player_name = request.GET['name']
        # Creates player object;
        new_player = Player.objects.create(username=player_name)
        # Assigns the id of the object to the player_id variable
        player_id = new_player.id
        # If game does not exist create's one
        if not Game.objects.get(id=game_id).exists():
            # Create's new game
            new_game = Game.objects.create(is_game_waiting=True, is_game_running=False)
            team_new_name = random_name()
            new_team = Team.objects.create(team_name=team_new_name, score=0, game_session=new_game.id)
        else:
            # Joins an exisint game
            new_game = Game.objects.get(id = game_id)
        # Id assignation
        game_id = new_game.id
    # Returns to team room view/page parsing the player_id and game_id as argument  
    return HttpResponseRedirect(reverse('app:team_creation'), kwargs={'player_id' : player_id, 'game_id' : game_id})

def team_creation(request, game_id, player_id):
    new_team_name = random_name()
    game_instance = Game.objects.get(id=game_id)
    player = Player.objects.get(player_id)
    if not Team.objects.filter(game_session=game_instance).exists() and not Team.objects.filter(team_name=new_team_name).exists():
        new_team_name = random_name()
        new_team = Team.objects.create(team_name=new_team_name,score=0,game_session=game_instance, players=player)
        team_id = new_team.id
    else:
        print('In design')
    return HttpResponseRedirect(reverse('app:game_room'), kwargs={'team_id' : team_id})


# This function assigns and distributes the teams using the game instance and the player's id 
# as inputs to create the team objects
def game_room(request, game_id):
    # Get game instance and player
    game_instance = Game.objects.get(id=game_id)
    player = Player.objects.get(player_id)
    
    return render(request, 'app/team_room.html', context)

# page with auto-refreshing list of games available for joining
def game_list(request):

    game_list = Game.objects.filter(is_game_waiting=True, is_game_running=False)

    context = { 'game_list':game_list }
    return render(request, 'app/game_list.html', context)

# join list of existing room
def game_session(request):
    
    game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)
    player_list = Player.objects.filter(game=game)

    context = { 'player_list':player_list }
    return render(request, 'app/game_session.html', context)
# create a waiting room   
def waiting_room(request, host):
    context = {"host": host}
    return render(request, "app/waiting_room.html", context)

def start_page(request):
    context = {}
    return render(request, "app/start_page.html", context)

def host_player_registration_form(request):
    if request.method == 'POST':
        # Assigns the form input to the players name
        player_name = request.POST['username']
        new_game = Game.objects.create()
        host = Player.objects.create(username=player_name,is_host=True,game=new_game)
    return HttpResponseRedirect(reverse('app:waiting_room', kwargs={'host': host.username}))

def join_player_registration_form(request):
    if request.method == 'POST':
        player_name = request.POST['username']
    return HttpResponseRedirect(reverse('app:start_page'))

def question_clue_spectrum(request):
    context = {}
    return render(request, "app/question_clue_spectrum.html", context)

def clue_form(request):
    if request.method == 'Post':
        player_clue = request.POST['clue']
    return HttpResponseRedirect(reverse('app:question_clue_spectrum'))

def game_end(request):
    context = {}
    return render(request, "app/game_end.html", context)

def team_score(request):
    team_name = request.GET['team_name']
    team_scores = Team.objects.filter(name__startswith=team_name)
    context = {"team_scores": team_scores}
    return HttpResponseRedirect(reverse('app:game_end'))