from django.db import models

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
        return f"{str(self.game_id)} {self.room_key} {self.is_game_active} {self.players} {self.created_at} {self.updated_at}"

class GameTurn(models.Model):
    team_id = models.ForeignKey("Team", on_delete=models.CASCADE)
    session_id = models.ForeignKey("Game", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    clue_giver = models.ForeignKey("User", on_delete=models.CASCADE)
    clue_given = models.CharField(max_length=100)
    game_answer = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    team_answer = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team_id} {self.session_id} {self.question} {self.clue_giver} {self.clue_given} {self.game_answer} {self.created_at} {self.team_answer}"

            

