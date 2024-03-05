from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
     # Make email required and has to be unique in the database
     email = models.EmailField(unique=True, blank=False)