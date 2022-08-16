from unicodedata import name
from unittest import expectedFailure
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
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

# When a player wants to play he/she has to type a username and select start/join.
# creating the player objects
# When a player wants to play the game selects "Start Game" or "Join game"
# the player is redirected to this function where the game objects are created
def start_page(request):
    context = {}
    return render(request, "wavelength/start_page.html", context)

def player_registration_form(request):
    if request.method == 'POST':
        # Assigns the form input to the players name
        player_name = request.POST['name']
    return HttpResponseRedirect(reverse('app:start_page'))
