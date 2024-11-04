from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    def __str__(self):
        return self.username
    
class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=25)
    priority = models.IntegerField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()

