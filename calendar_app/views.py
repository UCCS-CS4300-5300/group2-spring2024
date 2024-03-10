from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .models import *
from .forms import TaskForm

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'calendar_app/index.html')



def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            task = form.save()
            print(task.id)
            return redirect('/')
    else:
        form = TaskForm()

    context = {'form': form}
    return render(request, 'calendar_app/add_task_form.html', context)




def WeekView(request):
    return render(request, 'calendar_app/week_view.html')
# Registration form / login
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('calendar_app/accounts/index.html') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendar_app/accounts/register.html', {'form': form})
