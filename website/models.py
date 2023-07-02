from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, related_name='data', on_delete=models.CASCADE)
    question = models.TextField(max_length=6000)
    answer = models.TextField(max_length=6000)
    language = models.CharField(max_length=40)

    def __str__(self):
        return self.question

