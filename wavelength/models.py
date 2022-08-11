from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Question_history(models.Model):
  player = models.OneToOneField(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE) //connect to Question model