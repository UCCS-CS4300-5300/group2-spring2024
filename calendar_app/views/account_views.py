from typing import Any

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from .. import forms  # Import forms from the forms.py file up a directory


def login_view(request):
    context = {
        'title': 'Login',
        'button_text': 'Login',
    }
    return render(request, 'calendar_app/login.html', context)

# Registration form / login


def register(request):
    if request.method == 'POST':
        # Use forms.CustomUserCreationForm
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('index'))
    else:
        form = forms.CustomUserCreationForm()  # Use forms.CustomUserCreationForm
    return render(request, 'calendar_app/accounts/register.html', {'form': form})
