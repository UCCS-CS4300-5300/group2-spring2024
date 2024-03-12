from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Category, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'deadlineDay', 'deadlineTime', 'category', 'duration', 'status')

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
