# from asyncio.windows_events import NULL
import time
from unicodedata import name
from unittest import expectedFailure
from xml.dom import UserDataHandler
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from .models import *
import random
import re
from random import choice

teams_placeholder = {}

def index(request):   
    return render(request, 'app/index.html')

def room(request, room_name):
    username= request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]

    context = {'room_name' : room_name, 'username' : username, 'messages' : messages}
    return render(request, 'app/room.html', context)

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

def random_spectrum():
    # open the spectrum csv file
    with open("app/static/txt/spectrum.csv") as f:
        # Assigns all the lines
        spectrum_list = f.readlines()
        # Random assignation of a single spectrum from the list
        spectrum_name = spectrum_list[random.randint(0,len(spectrum_list))]
    # Returns a spectrum name
    return spectrum_name
    
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

def team_creation(request, game_id, player_id):
    print(player_id)
    current_player = Player.objects.get(id=player_id)
    print('--------------------------------start--------------------------------')
    if current_player.team is None and current_player.is_host == True:
        # print(current_player.team.id)
        print("****************************if************************************")
        print(current_player.team)
        # Stores the name of all the players
        player_names = []
        # empty list that will store all the team names
        team_names=[]
        ############################## GAME ################################
        # Obtain the game instance
        game_instance = Game.objects.get(id=game_id)
        # Number of players in game
        players = Player.objects.filter(game=game_id)
        # Game instance has started and is no longer waiting for players 
        game_instance.is_game_waiting = False
        # Game is running
        game_instance.is_game_running = True
        game_instance.save()
        ####################################################################

        # Checks for number of players before assigning teams
        if len(players) > 5:
            # Calculating the amount of teams and distributions
            # number of players/4 players per team and +1 to round number
            print("***************************************************************")
            print("Multiple teams")
            number_of_teams = int(players.count()/4)+1
            print(number_of_teams)
            print("***************************************************************")
        else: 
            # Single team
            print("***************************************************************")
            print("Single team")
            number_of_teams = 1
            print(number_of_teams)
            print("***************************************************************")

        print("***************************************************************")
        print(" This is a print for Teams algorithm confirmation only for debugging")
        print("game = " +str(game_instance.id))
        print("players = "+str(len(players)))
        print("teams =" +str(number_of_teams))
        print("teammates = " +str(int(len(players)/number_of_teams)))
        print("***************************************************************")

        ########### this can improve into the same random_name function. TBD ##########
        # All player names assignation,
        for player in players:
            # appends the players name
            player_names.append(player.username)
            print(player)
        
        # appends the team names based on the number of teams
        for i in range(0,number_of_teams):
            # assigns a random name to name
            name = random_name()
            team_names.append(name)

        # Dictionary with the sorted teams
        teams = get_teams(team_names, player_names)
        print("***************************************************************")
        print(teams)
        print("***************************************************************")
        ###############################################################################
        
        # List comprehension
        for key, value in teams.items():
            print(key)
            create_team = Team.objects.create(name=key, game=game_instance)
            print(create_team)
            for member in value:
                team_member = Player.objects.get(username=member)
                print(team_member.id)
                team_member.team=create_team
                team_member.save()
                print("***************************************************************")
            
            usr=Player.objects.get(id=player_id)
            game_id=usr.game.id
            team_id=usr.team.id

    else:
        print("****************************else************************************")
        print('begin tread')
        game_id=current_player.game.id
        team_id=current_player.team.id

    return HttpResponseRedirect(reverse('app:team_page', kwargs={'game_id' : game_id, 'team_id' : team_id, 'player_id': player_id }))

# AC: Team page will print all the members in the team 
def team_page(request, game_id, team_id, player_id):
    print(game_id)
    # game_id = Game.objects.get(id=game_id).id
    # print(game)
    player = Player.objects.get(id=player_id)
    team = Team.objects.filter(game=game_id)
    # team_id = Team.objects.get(id=team_id)
    teammates = Player.objects.filter(game=player.game)

    context = {'team':team, 'player':player, 'teammates':teammates,'team_id': team_id, 'game_id' : game_id}
    return render(request, "app/team_page.html",context)

# page with auto-refreshing list of games available for joining
# the ** before the keword argument means that the argument is not required
def game_list(request, **player_id):
    # assigns the argument to a variable 
    received_player = player_id
    # Confirms that the argument was recieved
    if not player_id:
        # Query all the games
        game_list = Game.objects.all()
        # assigns all the games to the Context
        context = { 'game_list':game_list}
        
    else:
        #If the keyword argument is received we get the information of the current player 
        current_player = Player.objects.get(id=received_player['player_id'])
        game_list = Game.objects.filter(is_game_waiting=True, is_game_running=False)
        context = { 'game_list':game_list , 'current_player':current_player}

    return render(request, 'app/game_list.html', context)

# AC: Player-game assignation, this function will assign the players to the game session 
def player_game_assignation(request, game_id, **player_id):
    # Assigns dictionary to current player variable
    current_player= player_id
    print(current_player)
    # Catches the joining player
    joining_player = Player.objects.get(id=current_player['player_id'])
    # Gets the current game
    player_room = Game.objects.get(id=game_id)
    # Assigns the game to the player
    joining_player.game = player_room
    # Save the dataset
    joining_player.save()
    # Passes the game id as an argument
    game_id = player_room.id
    # Passes the game id as an argument
    player_id = joining_player.id

    return HttpResponseRedirect(reverse('app:game_session', kwargs={'game_id':game_id, 'player_id':player_id}))

# join list of existing room
def game_session(request, game_id, player_id):
    # game_id = request.GET.get('game_id')
    game = Game.objects.get(id=game_id)
    player = Player.objects.get(id=player_id)
    print('********')
    print(player.username + ' from views')
    print('********')
    player_list = Player.objects.filter(game=game)
    context = { 'player_list' : player_list, 'game' : game, 'game_id' : game_id, 'player':player }
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
        # check if the player is created, if yes return True, if not create player
        host, created = Player.objects.get_or_create(username=player_name)
        player_id = host.id
        # save the player
        host.save()
        player = host.id
        # store all players from player model
        players = Player.objects.all()
        # passing players and form input information into context 
        context = {"players": players, "player_name": player_name}
        # check if the player already exist
        if created is True:
            # if player not exist, create a game then as a host:
            new_game = Game.objects.create()
            # save the new game
            new_game.save()
            # assign new game id to game_id
            game_id = new_game.id
            # assign is_host field value to the player
            host.is_host = True
            # assign game field value to the player
            host.game = new_game
            # save the player information
            host.save()
            
        # if the player already exist
        else:
            # render start page and pass context to start page
            return render(request, "app/start_page.html", context)
    # return response to game_session page, pass game_id key argument to it
    return HttpResponseRedirect(reverse('app:game_session', kwargs={'game_id': game_id, 'player_id':player_id}))

def join_player_registration_form(request):
    if request.method == 'POST':
        player_name = request.POST['username']
        join_player, created = Player.objects.get_or_create(username=player_name)
        join_player.save()
        players = Player.objects.all()
        context = {"players": players, "player_name": player_name}
        if created == True:
            join_player.is_host = False
            player_id = join_player.id
        else:
           return render(request, "app/start_page.html", context)
    return HttpResponseRedirect(reverse('app:game_list', kwargs={'player_id':player_id}))
    # return HttpResponse("form success")

def question_clue_spectrum(request, game_id, team_id, player_id):
    player = Player.objects.get(id=player_id)
    questions = Question.objects.all()
    random_question = choice(questions)
    random_question2 = choice(questions)
   
    # check if random_question == random_question2
    if random_question == random_question2:
        random_question = choice(questions)
        if random_question == random_question2:
            random_question = choice(questions)                                                                                                                                        
    left_spectrum = random_question.left_spectrum
    right_spectrum = random_question.right_spectrum
    left_spectrum2 = random_question2.left_spectrum
    right_spectrum2 = random_question2.right_spectrum
    # save the generated question into QuestionHistory
    players = Player.objects.all()
    player = choice(players)
    # question_history = QuestionHistory.objects.create(player=player, question=random_question)
    print("1111111111111111111111111111111111111")
    # print(question_history)
    print("1111111111111111111111111111111111111")
    context = {"left_spectrum": left_spectrum, "right_spectrum": right_spectrum, "left_spectrum2": left_spectrum2, "right_spectrum2": right_spectrum2, 'team_id' : team_id, 'player_id' : player_id, 'player' : player}
    return render(request, "app/question_clue_spectrum.html", context)
    
# clue form function
def clue_form_one(request):
    player_clue1 = request.POST['clue1']
    print("00000000000000000000000000000000000000000000000")
    print(player_clue1)
    print("00000000000000000000000000000000000000000000000")
    return HttpResponse(status=204)

def clue_form_two(request):
    player_clue2 = request.POST['clue2']
    print("00000000000000000000000000000000000000000000000")
    print(player_clue2)
    print("00000000000000000000000000000000000000000000000")
    return HttpResponse(status=204)

def game_end(request):
    context = {}
    return render(request, "app/game_end.html", context)

def team_score(request):
    team_name = request.GET['team_name']
    team_scores = Team.objects.filter(name__startswith=team_name)
    context = {"team_scores": team_scores}
    return HttpResponseRedirect(reverse('app:game_end'))

def game_turn(request):
    # game_turn spectrum has to be from team members
    
    
    # check if spectrum already be used
    # current_question = GameTurn.objects.get(question=)


    questions = Question.objects.all()
    random_question = choice(questions)                                                                                                                                                   
    left_spectrum = random_question.left_spectrum
    right_spectrum = random_question.right_spectrum
  
    # pass player clue to game_trun page
    # clue = player_clue
    # give left and right spectrum as context
    context = {"left_spectrum": left_spectrum, "right_spectrum": right_spectrum}
    question = Question.objects.create(left_spectrum=left_spectrum, right_spectrum=right_spectrum)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(question)
    print(left_spectrum)
    print(right_spectrum)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # render game_turn page
    return render(request, "app/game_turn.html", context)

# save the already used spectrum into a dictionary
def question_save(request, left_spectrum, right_spectrum):
    question = Question.objects.create(left_spectrum=left_spectrum, right_spectrum=right_spectrum)
    print("000000000000000000000000000000000")
    print(question)
    print("000000000000000000000000000000000")
    return HttpResponseRedirect(reverse('app:game_turn'))

def question_response_form(request):
    question_response = request.POST['question_response']
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(question_response)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    return HttpResponseRedirect(reverse('app:game_end'))

 
def scale(request):
    context = {}
    return render(request, "app/scale.html", context)

# def consumerView(game_id, player_id):
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

def dashboard(request):
    context = { }

    return render(request, "app/dashboard.html", context)

def dashboard_games(request):
    context = { }

    return render(request, "app/dashboard_games.html", context)

def dashboard_players(request):
    context = { }

    return render(request, "app/dashboard_players.html", context)

def dashboard_teams(request):
    context = { }

    return render(request, "app/dashboard_teams.html", context)

def dashboard_questions(request):
    context = { }

    return render(request, "app/dashboard_questions.html", context)

def dashboard_player_clues(request):
    context = { }

    return render(request, "app/dashboard_player_clues.html", context)