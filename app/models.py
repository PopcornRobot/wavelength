from django.db import models

# Create your models here.

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
