from statistics import mode
from django.db import models


# This models is only to enable the Game, the game's id will be used as the session ID required for the teams & game turn creation
class Game(models.Model):
    is_game_waiting = models.BooleanField(default=True)
    is_game_running = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" is the game open: {self.is_game_waiting}, The game status is: {self.is_game_running}, created: {self.created_at}, updated: {self.updated_at}"


# This models will store the information of the players , team name and scores
class Team(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #connect to Game model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #consider adding field game_host: player with privilege to start a game

    def __str__(self):
        return f" the team name is: {self.name}, the team's score is:{self.score}, the current game is: {self.game}, created: {self.created_at}, updated: {self.updated_at}"

# This model stores the player's information. The information consists on the team and the game that the player is either staring or joining
# The team object is populated once the host player "Starts the Game"
# Te game object is populated once the player selects the join/start a new game.
class Player(models.Model):
    username = models.CharField(max_length = 20)
    is_host = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" the current player is: {self.username}, is this the host: {self.is_host}, the players team is: {self.team}, the player's game is: {self.game}, created: {self.created_at}, updated: {self.updated_at}"


# This model stores the left & right spectrums indicators 
class Question(models.Model):
    left_spectrum = models.CharField(max_length=100)
    right_spectrum = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" the left spectrum is: {self.left_spectrum}, the right spectrum is: {self.right_spectrum}, created: {self.created_at}, updated: {self.updated_at}"

# This will store the questions previously assigned
class QuestionHistory(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE) #connect to Player model
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #connect to Question model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" the player assigned with the question is: {self.player}, used question: {self.question}, created: {self.created_at}, updated: {self.updated_at}"

# This model stores the game history (responses, questions, teams and clues)
class GameTurn(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    clue_giver = models.ForeignKey(Player, on_delete=models.CASCADE) # Clue is the response that the polayer provides 
    clue_given = models.CharField(max_length=100) 
    question_answer = models.IntegerField(default=0) # Question answer is randomly assigned
    team_answer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" the team in the room is:{self.team}, the game is: {self.game}, the question is:{self.question}, the clue giver is: {self.clue_giver}, the previous clue is: {self.clue_given}, the current question answer is: {self.question_answer}, the team answer is {self.team_answer}, created: {self.created_at}, updated: {self.updated_at}"
