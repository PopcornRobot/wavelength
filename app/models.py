from django.db import models

# Create your models here.
class Question(models.Model):
    # user = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    question = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
       