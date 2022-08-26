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
def team_creation(request, game_id=1):
    # Obtain the game instance
    game_instance = Game.objects.get(id=game_id)
    # Number of players in game
    players = Player.objects.filter(game=game_instance)
    # Calculating the amount of teams and distributions
    # number of players/4 players per team and +1 to round number
    number_of_teams = int(players.count()/4)+1
    print(number_of_teams)
    team_mates = int(len(players)/number_of_teams)

    print("players = "+str(len(players)))
    print("teams =" +str(number_of_teams))

    team_names=[]
    for i in range(0,number_of_teams):
        name = random_name()
        # print(name)
        team_names.append(name.removesuffix("\n"))
    
    # Dictionary with the sorted teams
    teams = get_teams(team_names, players)

    # List comprehension
    for key, values in teams.items():
        # Creating new team
        new_team = Team.objects.create(name=key, game=game_id)
        # Get players name
        player_assignation = Player.objects.get(username= [p for p in values])
        # Player's object stores the team created
        player_assignation.team=new_team
        # Saves dataset
        player_assignation.save()

    return HttpResponseRedirect(reverse('app:team_page', kwargs={'game_instance' : game_instance}))

# AC: Team page will print aall the members in the team 
def team_page(request):
    # teams = Team.objects.get(game=game_instance)
    teammates = None
    context = {'teammates':teammates}
    return render(request, "app/team_page.html",context)


# page with auto-refreshing list of games available for joining
def game_list(request):

    game_list = Game.objects.filter(is_game_waiting=True, is_game_running=False)

    context = { 'game_list':game_list }
    print(game_list)
    return render(request, 'app/game_list.html', context)

# join list of existing room
def game_session(request, current_game):
    # host.game.id
    # game_id = request.GET.get('game_id')
    game = Game.objects.get(id=current_game)
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
        print(host.id)
        print(new_game.id)
        current_game = new_game.id
    return HttpResponseRedirect(reverse('app:game_session', kwargs={'current_game': current_game}))

def join_player_registration_form(request):
    if request.method == 'POST':
        player_name = request.POST['username']
        print(player_name)
    return HttpResponseRedirect(reverse('app:game_list'))

# def player_game_assignment(request) need to work on this function
def player_game_assignment(request):
    
    return HttpResponseRedirect(reverse('app:game_session'))

def question_clue_spectrum(request):
    context = {}
    return render(request, "app/question_clue_spectrum.html", context)

def clue_form(request):
    if request.method == 'Post':
        player_clue = request.POST['clue']
    return HttpResponseRedirect(reverse('app:question_clue_spectrum'))

def game_end(request):
    team1 = Team.objects.get()
    team2 = Team.objects.get()
    context = {}
    return render(request, "app/game_end.html", context)

def team_score(request):
    team_name = request.GET['team_name']
    team_scores = Team.objects.filter(name__startswith=team_name)
    context = {"team_scores": team_scores}
    return HttpResponseRedirect(reverse('app:game_end'))