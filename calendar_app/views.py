from .models import *
from .forms import TaskForm, CustomUserCreationForm
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login


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
            return redirect('calendar_app/accounts/index.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendar_app/accounts/register.html', {'form': form})


def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            task = form.save()
            return redirect('/')
    else:
        form = TaskForm()

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)

# class TaskDetailView(generic.DetailView):
#     model = Task
#
# class TaskListView(generic.ListView):
#     model = Task

# def updateTask(request, task_id ):
#     task = Task.objects.get(pk=task_id)
#     form = TaskForm(instance=task)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#         return redirect('task-detail', task.id)
#
#     context = {'form': form}
#     return render(request, 'calendar_app/task_form.html', context)
#
# def deleteTask(request, task_id):
#     task = Task.objects.get(pk=task_id)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('/')
#
#     context = {'task': task}
#     return render(request, 'calendar_app/delete_task_form.html', context)

