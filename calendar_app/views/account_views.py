from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from typing import Any
from django.utils.safestring import mark_safe
from .. import forms  # Import forms from the forms.py file up a directory

# Registration form / login
def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)  # Use forms.CustomUserCreationForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = forms.CustomUserCreationForm()  # Use forms.CustomUserCreationForm
    return render(request, 'calendar_app/accounts/register.html', {'form': form})