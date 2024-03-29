from django.shortcuts import redirect, render
from django.views import generic

from ..forms import TaskForm
from ..models import Task


class TaskDetailView(generic.DetailView):
    model = Task

class TaskListView(generic.ListView):
    model = Task

def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            task = form.save()
            return redirect('index')
    else:
        form = TaskForm()

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)

def updateTask(request, task_id):
    task = Task.objects.get(pk=task_id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('task-detail', task.id)

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)

def deleteTask(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')

    context = {'task': task}
    return render(request, 'calendar_app/delete_task_form.html', context)
