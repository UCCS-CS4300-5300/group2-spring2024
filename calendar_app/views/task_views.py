from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import get_objects_for_user

from ..forms import TaskForm
from ..models import CustomUser, Task


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(permission_required_or_403('view_task', (Task, 'pk', 'pk')), name='dispatch')
class TaskDetailView(generic.DetailView):
    model = Task


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TaskListView(generic.ListView):
    model = Task

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'calendar_app.view_task').order_by('deadlineDay', 'deadlineTime')


@login_required(login_url='/login/')
def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            # Save the form data to the database
            form.instance.user = request.user
            task = form.save()
            return redirect('index')
    else:
        form = TaskForm(user=request.user)

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)


@login_required(login_url='/login/')
@permission_required_or_403('change_task', (Task, 'pk', 'task_id'))
def updateTask(request, task_id):
    task = Task.objects.get(pk=task_id)
    form = TaskForm(instance=task, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
        return redirect('task-detail', task.id)

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)


@login_required(login_url='/login/')
@permission_required_or_403('delete_task', (Task, 'pk', 'task_id'))
def deleteTask(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')

    context = {'task': task}
    return render(request, 'calendar_app/delete_task_form.html', context)
