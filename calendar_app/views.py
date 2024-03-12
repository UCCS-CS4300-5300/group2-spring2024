from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.urls import reverse

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'calendar_app/index.html')

# Registration form / login
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('index'))  # Redirect to the index page
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendar_app/accounts/register.html', {'form': form})
