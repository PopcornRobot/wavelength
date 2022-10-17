# from asyncio.windows_events import NULL
from unicodedata import name
from unittest import expectedFailure
from django.http import HttpResponseRedirect
from xml.dom import UserDataHandler
from django.shortcuts import render
from django.urls import reverse
from .models import Game, Team, Player, Question, QuestionHistory, GameTurn, Message
import random
from random import choice

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

def random_spectrum():
    # open the spectrum csv file
    with open("app/static/txt/spectrum.csv") as f:
        # Assigns all the lines
        spectrum_list = f.readlines()
        # Random assignation of a single spectrum from the list
        spectrum_name = spectrum_list[random.randint(0,len(spectrum_list))]
    # Returns a spectrum name
    return spectrum_name
    
# This function assignes the players to the teams, taking the number of possible teams and the amount of players as arguments
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

# This function will be enable only by the host
# NOTE: Create a player joining argument to track who joins and use it as URL #
def team_creation(request, game_id, player_id):
    print(player_id)
    current_player = Player.objects.get(id=player_id)

    if current_player.team is None and current_player.is_host == True:
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
            number_of_teams = int(players.count()/4)+1
        else: 
            # Single team")
            number_of_teams = 1

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
        ###############################################################################
        
        # List comprehension
        for key, value in teams.items():
            create_team = Team.objects.create(name=key, game=game_instance)
            for member in value:
                team_member = Player.objects.get(username=member)
                team_member.team=create_team
                team_member.save()
            
            usr=Player.objects.get(id=player_id)
            game_id=usr.game.id
            team_id=usr.team.id

    else:
        game_id=current_player.game.id
        team_id=current_player.team.id

    return HttpResponseRedirect(reverse('app:team_page', kwargs={'game_id' : game_id, 'team_id' : team_id, 'player_id': player_id }))

# Team page will print all the members in the team 
def team_page(request, game_id, team_id, player_id):
    player = Player.objects.get(id=player_id)
    team = Team.objects.filter(game=game_id)
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

# Player-game assignation, this function will assign the players to the game session 
def player_game_assignation(request, game_id, **player_id):
    # Assigns dictionary to current player variable
    current_player= player_id
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
    player_list = Player.objects.filter(game=game)
    context = { 'player_list' : player_list, 'game' : game, 'game_id' : game_id, 'player':player }
    return render(request, 'app/game_session.html', context)

# create a waiting room   
def waiting_room(request, game_id):
    game = Game.objects.get(id=game_id)
    questions_left = GameTurn.objects.filter(game=game, team_answer=0)
    context = {"questions_left" : questions_left, 'game_id':game_id}
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
    all_question_history = QuestionHistory.objects.all()
    player = Player.objects.get(id=player_id)
    team = Team.objects.get(id=team_id)
    team_members = Player.objects.filter(team=team)
    questions = Question.objects.all()

    random_question = choice(questions)
    random_question2 = choice(questions)

    # Checks if the values exist and avoids repetead values withing the different teams
    if QuestionHistory.objects.filter(question=random_question).exists() or QuestionHistory.objects.filter(question=random_question2).exists(): 
        random_question = choice(questions)
        random_question2 = choice(questions)
        while random_question == random_question2:
            random_question = choice(questions)
            random_question2 = choice(questions)
    else:
        while random_question == random_question2:
            random_question = choice(questions)
            random_question2 = choice(questions)

    left_spectrum = random_question.left_spectrum
    right_spectrum = random_question.right_spectrum
    left_spectrum2 = random_question2.left_spectrum
    right_spectrum2 = random_question2.right_spectrum
    # save the generated question into QuestionHistory
    question_history = QuestionHistory.objects.create(player=player, question=random_question)
    question_history2 = QuestionHistory.objects.create(player=player, question=random_question2)
   
    # save the generate answer into GameTurn
    generated_random_question_answer = random.randint(1, 100)
    generated_random_question_answer_two = random.randint(1, 100)
   
    # context = {"left_spectrum": left_spectrum, "right_spectrum": right_spectrum, "left_spectrum2": left_spectrum2, "right_spectrum2": right_spectrum2, 'team_id' : team_id, 'player_id' : player_id, 'player' : player, 'game_id' : game_id, 'random_question' : random_question, 'random_question2' : random_question2, 'team_members' : team_members, 'generated_random_question_answer': generated_random_question_answer, 'generated_random_question_answer_two': generated_random_question_answer_two}
    context = {"left_spectrum": left_spectrum, "right_spectrum": right_spectrum, "left_spectrum2": left_spectrum2, "right_spectrum2": right_spectrum2, 'team_id' : team_id, 'player_id' : player_id, 'player' : player, 'game_id' : game_id, 'random_question' : random_question, 'random_question2' : random_question2, 'team_members' : team_members, 'generated_random_question_answer': generated_random_question_answer, 'generated_random_question_answer_two': generated_random_question_answer_two,}
    return render(request, "app/question_clue_spectrum.html", context)
    
# submit clue and create new GameTurn object
def clue_form(request):
    team_id = request.get('team')
    team = Team.objects.get(id=team_id)
    game_id = request.get('game')
    game = Game.objects.get(id=game_id)
    question_id = request.get('question')
    question = Question.objects.get(id=question_id)
    player_name = request.get('username')
    player = Player.objects.get(username=player_name)
    clue = request.get('clue')
    question_answer = request.get('value')

    new_game_turn = GameTurn.objects.create(team=team, game=game, question=question, player=player, clue_given=clue, question_answer=question_answer)
    print('created GameTurn ' + str(new_game_turn))
    
def game_end(request, game_id):
    average_score=[]
    points = []
    results={}
    game = Game.objects.get(id=game_id)
    teams_in_game = Team.objects.filter(game = game).order_by('-score')

    # Calculates the average questions
    for team in teams_in_game:
        total_team_clues = Player.objects.filter(game=game, team=team).count() * 2
        total_team_points = team.score
        team_names = team.name
        average = total_team_points / total_team_clues
        average_score.append(average)
        results = dict(zip(teams_in_game, average_score))

    context = { "results":results, "total_team_clues":total_team_clues,"teams_in_game": teams_in_game, "game":game }
    return render(request, "app/game_end.html", context)

def game_turn(request, game_id, team_id, player_id):
    game = Game.objects.get(id=game_id)
    team = Team.objects.get(id=team_id)
    player = Player.objects.get(id=player_id)

    team_members = Player.objects.filter(team=team)
    team_size = team_members.count()

    unanswered_clues = GameTurn.objects.filter(team=team, team_answer=0).order_by('player').first()
    clue = unanswered_clues
    turn_id = clue.id

    context = {'turn_id': turn_id, 'game': game, 'team': team, 'player': player, 'clue': clue, 'game_id': game_id, 'team_id': team_id, 'player_id':player_id, 'team_size': team_size, 'team_members':team_members, 'unanswered_clues': unanswered_clues }

    return render(request, "app/game_turn.html", context)

def game_result(request, game_id, team_id, player_id, turn_id):
    game_turn = GameTurn.objects.get(id=turn_id)
    question = game_turn.question
    team = Team.objects.get(id=team_id)
    turns_remaining = GameTurn.objects.filter(team=team, team_answer=0).count()

    team_answer = game_turn.team_answer
    question_answer = game_turn.question_answer

    context = {'team_answer':team_answer, 'question_answer': question_answer, "game_turn" : game_turn, "question" : question, "turns_remaining" : turns_remaining, "game_id" : game_id, "team_id" : team_id, "player_id" : player_id}
    return render(request, "app/game_result.html", context)

def leaving_user(request, player_id):
    # Function deletes the user and send's it to the start page
    Player.objects.get(id=player_id).delete()
    return HttpResponseRedirect(reverse('app:start_page'))

# save the already used spectrum into a dictionary
def question_save(request, left_spectrum, right_spectrum):
    question = Question.objects.create(left_spectrum=left_spectrum, right_spectrum=right_spectrum)

    return HttpResponseRedirect(reverse('app:game_turn'))

def team_answer_response_form(request, game_id, team_id, player_id, turn_id):
  
    if request.method == 'POST':
        team_answer_form = request.POST['slider']
        question = GameTurn.objects.get(id=turn_id).question_answer      
        team = Team.objects.get(id=team_id)
        difference = abs(question - int(team_answer_form))
        team_answer = GameTurn.objects.get(id=turn_id).team_answer

        #below prevents the websockets from adding the team_answer mutiple times
        if team_answer == 0:
            team_answer = GameTurn.objects.filter(id=turn_id).update(team_answer=team_answer_form)
            # below records score based on pre-defined threshold    
            if difference <= 6:
                team.score += 4
            elif 7 <= difference <=12:
                team.score += 3
            elif 13 <= difference <=18:
                team.score +=2
            elif 19 <= difference <=24:
                team.score  +=1
            team.save()

    return HttpResponseRedirect(reverse('app:game_result', kwargs={'game_id':game_id, 'team_id':team_id, 'player_id':player_id,'turn_id':turn_id}))
 
def scale(request):
    context = {}
    return render(request, "app/scale.html", context)

def dashboard(request):
    context = {}

    return render(request, "app/dashboard.html", context)

def dashboard_games(request):
    games = Game.objects.all()
    context = { "games":games }

    return render(request, "app/dashboard_games.html", context)

def dashboard_players(request):
    players = Player.objects.all()
    context = { "players":players }

    return render(request, "app/dashboard_players.html", context)

def dashboard_teams(request):
    teams = Team.objects.all()
    context = { "teams":teams }

    return render(request, "app/dashboard_teams.html", context)

def dashboard_questions(request):
    questions = Question.objects.all()
    context = { "questions":questions }

    return render(request, "app/dashboard_questions.html", context)

# Need to add data into player_clue to avoid error:
def dashboard_player_clues(request):
    player_clues = []
    gameturn = GameTurn.objects.all()
    for clue in gameturn:
        player_clue = clue['clue_given']
    player_clues.append(player_clue)
    context = { "player_clues":player_clues }

    return render(request, "app/dashboard_player_clues.html", context)

def cleaning_data_base(request, game_id):
    #Get all the objects
    if Game.objects.filter(id=game_id).exists():
        game=Game.objects.get(id=game_id)
        players=Player.objects.filter(game=game).delete()
        teams=Team.objects.filter(game=game).delete()
        game.delete()

    return HttpResponseRedirect(reverse('app:start_page'))
def game_tutorial(request):
    context = {}
    return render(request, 'app/game_tutorial.html', context)
##########################################################################################