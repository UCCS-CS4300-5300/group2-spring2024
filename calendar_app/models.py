from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     # Make email required and has to be unique in the database
     email = models.EmailField(unique=True, blank=False)
class User(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# For use with Tasks
class Category(models.Model):
    category = models.IntegerField()

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    deadlineDay = models.DateField()
    deadlineTime = models.TimeField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    duration = models.DurationField()
    status = models.BooleanField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # Changed to use CustomUser instead of User
    def __str__(self):
        return self.name