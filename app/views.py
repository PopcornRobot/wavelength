from unicodedata import name
from unittest import expectedFailure
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from .models import *
import random

teams_placeholder = {}

def index(request):
    return HttpResponse("Hello, world")


########################################## JAJA! project starts here ################################################################

# AC: This function opens a file that stores a list of 250 team names and resturns a random name from the list
def random_name():
    # open the file
    with open("app/static/txt/team_names.csv") as f:
        # Assigns all the lines
        name_list = f.readlines()
        # Random assignation of a single name from the list
        new_name = name_list[random.randint(0,len(name_list))]
    # Returns a new randome name
    return new_name

# AC: This function assignes the players to the teams, taking the number of possible teams and the amount of players as arguments
def get_teams(team_names, players):
    # randomly shuffles all the players
    randomly_ordered_players = random.sample(players, len(players))
    # stores the number of possible teams
    number_of_teams = len(team_names)

    return {
        # Returns a list of players randomly assigned to the team index 
        # Slice the information into team with random name as first value and then seperates it by ":" 
        # and assigns as many players as they can fit per team [first player:second:third:team_number]
        team_names[i]: randomly_ordered_players[i::number_of_teams]
        for i in range(number_of_teams)
    }

# AC: This function will be enable only by the host
# NOTE: Create a player joining argument to track who joins and use it as URL #

def team_creation(request, player_game, player_id):
    # Stores the name of all the players
    player_names = []
    # Retrieve host
    host_player = Player.objects.get(id=player_id)
    # Number of players in game
    players = Player.objects.filter(game=player_game)
    # Obtain the game instance
    game_instance = Game.objects.get(id=player_game)
    # Game instance has started and is no longer waiting for players 
    game_instance.is_game_waiting = False
    # Game is running
    game_instance.is_game_running = True
    game_instance.save()
    
    # Checks for number of players before assigning teams
    if len(players) > 4:
        # Calculating the amount of teams and distributions
        # number of players/4 players per team and +1 to round number
        number_of_teams = int(players.count()/4)
        number_of_team_players = int(len(players)/number_of_teams)
    else:
        # Single team
        number_of_teams = 1

    # print("***************************************************************")
    # print(" This is a print for Teams algorithm confirmation only for debugging")
    # print("game = " +str(game_instance.id))
    # print("players = "+str(len(players)))
    # print("teams =" +str(number_of_teams))
    # print("teammates = " +str(number_of_team_players))
    # print("***************************************************************")

    # All player names assignation,
    for player in players:
        # appends the players name
        player_names.append(player.username)
    
    ########### this can improve into the same random_name function. TBD ##########
    # empty list that will store all the team names
    team_names=[]
    # appends the team names based on the number of teams
    for i in range(0,number_of_teams):
        # assigns a random name to name
        name = random_name()
        # appends the names and removes the suffix \n from the raw file
        team_names.append(name.removesuffix("\n"))
    ##########

    # Dictionary with the sorted teams
    teams = get_teams(team_names, player_names)
    # List comprehension
    for team_name, team_mates in teams.items():
        # Creating new team
        new_team = Team.objects.create(name=team_name, game=game_instance)
        # Search for the players names inside the team
        for participant in team_mates:
            # Gets the player based on the name and is assigned to team assignation
            team_assignation = players.get(username=participant)
            # Assigns the team to the player model
            team_assignation.team = new_team
            team_assignation.save()
            game_id = game_instance.id
            host_id = host_player.id
            
    return HttpResponseRedirect(reverse('app:team_page', kwargs={ 'host_id': host_id, 'game_id' : game_id}))

# AC: Team page will print aall the members in the team 
def team_page(request, host_id, game_id):

    host = Player.objects.get(id=host_id)
    teams = Team.objects.filter(game=game_id)
    players = Player.objects.filter(game=host.game)

    context = {'teams':teams, 'players':players}
    return render(request, "app/team_page.html",context)

# page with auto-refreshing list of games available for joining
def game_list(request, player_id):

    current_player = Player.objects.get(id=player_id)
    game_list = Game.objects.filter(is_game_waiting=True, is_game_running=False)

    context = { 'game_list':game_list , 'current_player':current_player}
    return render(request, 'app/game_list.html', context)

# AC: Player-game assignation, this function will assign the players to the game session 
def player_game_assignation(request, game_id, player_id):
    # Catches the joining player
    joining_player = Player.objects.get(id=player_id)
    # Gets the current game
    player_room = Game.objects.get(id=game_id)
    # Assigns the game to the player
    joining_player.game = player_room
    # Save the dataset
    joining_player.save()
    # Passes the game id as an argument
    game_id = player_room.id

    return HttpResponseRedirect(reverse('app:game_session', kwargs={'game_id':game_id}))

# join list of existing room
def game_session(request, game_id):
    # game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)
    player_list = Player.objects.filter(game=game)
    context = { 'player_list' : player_list, 'game' : game }
    return render(request, 'app/game_session.html', context)

# create a waiting room   
def waiting_room(request, host):
    context = {"host": host}
    return render(request, "app/waiting_room.html", context)

def start_page(request):
    context = {}
    return render(request, "app/start_page.html", context)

def host_player_registration_form(request):
    #############################################
    # Needs a condition to avoid repeated names #
    #############################################
    if request.method == 'POST':
        # Assigns the form input to the players name
        player_name = request.POST['username']
        new_game = Game.objects.create()
        host = Player.objects.create(username=player_name,is_host=True,game=new_game)
        game_id = new_game.id
        player_id = host.id
    return HttpResponseRedirect(reverse('app:game_session', kwargs={'game_id': game_id}))

def join_player_registration_form(request):
    #############################################
    # Needs a condition to avoid repeated names #
    #############################################
    if request.method == 'POST':
        player_name = request.POST['username']
        new_player= Player.objects.create(username=player_name, is_host=False)
        player_id = new_player.id
    return HttpResponseRedirect(reverse('app:game_list', kwargs={'player_id':player_id}))

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