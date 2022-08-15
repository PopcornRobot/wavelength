from django.db import models

class Question(models.Model):
    # user = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # unless we want to merge them, this model should have two CharFields: left_spectrum and right_spectrum
    question = models.CharField(max_length=50)

    def __str__(self):
        return self.question

# This models is only to enable the Game, the game's id will be used as the session ID required for the teams & game turn creation
class Game(models.Model):
    is_game_waiting = models.BooleanField(default=False)
    is_game_running = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.is_game_waiting} {self.is_game_running} {self.created_at} {self.updated_at}"
    
class Player(models.Model):
    username = models.CharField(max_length = 20)

    def __str__(self):
        return self.player

# This models will store the information of the players , team name and scores
class Team(models.Model):
    team_name = models.CharField(max_length=100)
    score = models.BooleanField(default=False)
    session_id = models.ForeignKey(Game, on_delete=models.CASCADE) #connect to Game model
    players = models.ForeignKey(Player, on_delete=models.CASCADE) #connect to Player model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.team_name} {self.score} {self.session_id} {self.players} {self.created_at} {self.updated_at}"

# TODO: will uncomment when models are finalize, temporary commented out
# class QuestionHistory(models.Model):
#     player = models.OneToOneField(Player, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE) #connect to Question model

#     def __str__(self):
#         return f "{self.player} {self.question}"

class GameTurn(models.Model):
    # team_id = models.ForeignKey("Team", on_delete=models.CASCADE)
    # session_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    # question = models.ForeignKey("Question", on_delete=models.CASCADE)
    # clue_giver = models.ForeignKey("User", on_delete=models.CASCADE)
    clue_given = models.CharField(max_length=100)
    game_answer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    team_answer = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_id} {self.session_id} {self.question} {self.clue_giver} {self.clue_given} {self.game_answer} {self.created_at} {self.team_answer}"

            

