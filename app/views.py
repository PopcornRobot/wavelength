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

# This function will be enable only by the host
def team_creation(request, game_id):
    # Obtain the game instance
    game_instance = Game.objects.get(id= game_id)
    # Number of players in game
    players = Player.objects.filter(game=game_instance)

    # if there are more than 4 players
    if players.count() > 4:
        
        # Verifies if the division has decimals
        if players.count()//3 == players.count()/3:
            # it does not have decimals
            # Stores the number of teams for the game
            teams_number = players.count()/3
        else:
            # it has decimals
            teams_number = int(players.count()/3)+1

        for number in teams_number:
            team_name = random_name()
            new_team = Team.objects.create(name=team_name, score=0, game=game_instance)
            for player in players:
                player.team = new_team
            
    else:
        # creates a single game
        # Creates random name
        team_name = random_name()
        # Creates a team
        new_team = Team.objects.create(name=team_name, score=0, game=game_instance)
        # Goes inside the filtered players
        for player in players:
            # Assigns the team id to the current players
            player.team = new_team.id

    return HttpResponseRedirect(reverse('app:team_page'), kwargs={'game_instance':game_instance})

# Team page will print aall the members in the team 
def team_page(request, game_instance):
    teams = Team.objects.get(game=game_instance)
    teammates = Player.objects.filter(team = teams)
    context = {'teammates':teammates}
    return render(request, "app/team_page.html",context)

###########################################################################################################
def test_team_page(request):
    context={}
    return render(request,"app/test_team_page.html",context)    
###########################################################################################################

# page with auto-refreshing list of games available for joining
def game_list(request):

    game_list = Game.objects.order_by('created_at')

    context = { 'game_list':game_list }
    return render(request, 'app/game_list.html', context)

def game_session(request):

    player_list = Team.objects.order_by('created_at')

    context = { 'player_list':player_list }
    return render(request, 'app/game_session.html', context)
    
def start_page(request):
    context = {}
    return render(request, "app/start_page.html", context)

def player_registration_form(request):
    if request.method == 'POST':
        # Assigns the form input to the players name
        player_name = request.POST['name']
    return HttpResponseRedirect(reverse('app:start_page'))
