from django.shortcuts import render
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


