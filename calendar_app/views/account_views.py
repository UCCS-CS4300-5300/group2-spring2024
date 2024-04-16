from typing import Any

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from .. import forms  # Import forms from the forms.py file up a directory


# Registration form / login
def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)  # Use forms.CustomUserCreationForm
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('index'))
    else:
        form = forms.CustomUserCreationForm()  # Use forms.CustomUserCreationForm
    return render(request, 'calendar_app/accounts/register.html', {'form': form})
