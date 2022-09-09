from statistics import mode
from django.db import models

class Game(models.Model):
    """
    This models is only to enable the Game, the game's id will be used as the session ID required for the teams & game turn creation
    """
    is_game_waiting = models.BooleanField(default=True)
    is_game_running = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.id
class Team(models.Model):
    """
    This models will store the information of the players , team name and scores
    """
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE) #connect to Game model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: consider adding field game_host: player with privilege to start a game

    def __str__(self):
        return self.name

class Player(models.Model):
    """
    This model stores the player's information. The information consists on the team and the game that the player is either staring or joining
    The team object is populated once the host player "Starts the Game"
    The game object is populated once the player selects the join/start a new game.
    """
    username = models.CharField(max_length = 20)
    is_host = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
class Question(models.Model):
    """
    This model stores the left & right spectrums indicators 
    """
    left_spectrum = models.CharField(max_length=100)
    right_spectrum = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" the left spectrum is: {self.left_spectrum}, the right spectrum is: {self.right_spectrum}"

class QuestionHistory(models.Model):
    """
    This will store the questions previously assigned
    """
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player

class GameTurn(models.Model):
    """
    This model stores the game history (responses, questions, teams and clues)
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)        # Clue is the response that the polayer provides 
    clue_given = models.CharField(max_length=100) 
    question_answer = models.IntegerField(default=0)                    # Question answer is randomly assigned
    team_answer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game, self.id

class Message(models.Model):
  username = models.CharField(max_length=255)
  room = models.CharField(max_length=255)
  content = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ('date_added',)