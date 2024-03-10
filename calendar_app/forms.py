from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Category
from django.contrib.auth import get_user_model


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'deadlineDay', 'deadlineTime', 'category', 'duration', 'status')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password']
