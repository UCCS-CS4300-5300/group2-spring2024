from colorfield.fields import ColorField
from colorfield.widgets import ColorWidget
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Category, CustomUser, Task


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'deadlineDay',
                  'deadlineTime', 'category', 'duration', 'status')

    def __init__(self, *args, **kwargs):
        filterUser = kwargs.pop('user', None)
        filterUser = filterUser if isinstance(filterUser, CustomUser) else None
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['category'].queryset = Category.objects.filter(
            user=filterUser)


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']
        widgets = {
            'color': forms.CharField(widget=ColorWidget)
        }
