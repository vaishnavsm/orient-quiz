from django.db import models
import uuid
# Create your models here.
class Profile(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    Name = models.CharField(max_length=100, default="")
    Phone_Number = models.CharField(max_length=20, default="")
    Email = models.CharField(max_length=100, default="")
    Played = models.BooleanField(default = False)
    Score = models.FloatField(default=0)
    ConsideredScore = models.FloatField(default=0)
    SolvedQns = models.CharField(max_length=1000, default="")
    Lives = models.IntegerField(default=3)
    def __str__(self):
        return self.Name+" "+str(self.Email)
    #id = models.AutoField()

class Question(models.Model):
    uid = models.UUIDField(default=uuid.uuid4)
    Question = models.CharField(max_length=1000, default="")
    Option_1 = models.CharField(max_length=100, default="")
    Option_2 = models.CharField(max_length=100, default="")
    Option_3 = models.CharField(max_length=100, default="")
    Option_4 = models.CharField(max_length=100, default="")
    Correct_Answer = models.IntegerField(default=0)
    Difficulty = models.IntegerField(default=1)
    #id = models.AutoField()