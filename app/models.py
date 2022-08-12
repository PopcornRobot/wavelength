from django.db import models

# Create your models here.

class Question(models.Model):
    # user = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    question = models.CharField(max_length=50)

    def __str__(self):
        return self.question

class GameRoom(models.Model):
    # game_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    room_key = models.CharField(max_length=100)
    is_game_active = models.BooleanField(default=False)
    players = models.IntegerField(default=0)
    teams = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.game_id) + " " + self.room_key + " " + str(self.is_game_active) + " " + str(self.players) + " " + str(self.created_at) + " " + str(self.updated_at)
    
class Player(models.Model):
    username = models.CharField(max_length = 20)

    def __str__(self):
        return self.player

class Question_history(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #connect to Question model

    def __str__(self):
        return self.player

