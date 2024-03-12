from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     # For task list and task detail we need user to have a list of tasks as its own model to be able to display all of them on a page task list easily and that model will require "def get_absolute_url(self): return reverse('task-detail', args=[str(self.id)])".
     # That will allow task_detail.html to have a link back to the list of all tasks for the user.
     # Make email required and has to be unique in the database
     email = models.EmailField(unique=True, blank=False)
class User(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# For use with Tasks
class Category(models.Model):
    name = models.CharField(max_length=20)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    deadlineDay = models.DateField()
    deadlineTime = models.TimeField()

    category = models.ForeignKey(Category,blank=True,null=True,on_delete=models.SET_NULL)
    duration = models.DurationField()
    status = models.BooleanField()
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE) # Changed to use CustomUser instead of User
    def __str__(self):
        return self.name