from django.shortcuts import render
from ..models import Task
from datetime import datetime

#from django.views import View
from django.db.models import Count

import matplotlib
matplotlib.use('Agg') # Prevent matplotlib runtimeerror
import matplotlib.pyplot as mplt

from io import BytesIO
import base64

from .display_views import get_date, get_prev_month, get_next_month

def graphMonthlyTasksCompleted(request, year=None, month=None, day=None):
    context = {}

    # Get current date
    currentDate = datetime.today()
    
    # Set current month and year to pass to template for display
    monthNames = ["January", "February", "March", "April", "May", "June", "July", 
                  "August", "September", "October", "November", "December"]
    currentYear = currentDate.year
    currentMonth = currentDate.month
    currentMonthName=monthNames[int(currentDate.month) - 1]
    context['monthAndYear'] = f'{currentMonthName} {currentYear}'

    # Set next and previous months
    day = get_date(request.GET.get('month', None))
    context['prevMonth'] = get_prev_month(day)
    context['thisMonth'] = f'month={currentYear}-{currentDate.month}'
    context['nextMonth'] = get_next_month(day)

    # Get completed (status=True) Task objects
    tasksCompleted = Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear,status=True).values('deadlineDay').annotate(numCompleted=Count('deadlineDay'))

    # Create graph with matplotlib
    # Number of tasks on y vs day completed on x
    yAxis = [result['numCompleted'] for result in tasksCompleted]
    xAxis = [result['deadlineDay'] for result in tasksCompleted]

    # Set aspect ratio, y axis scale, and labels
    mplt.figure(figsize=(16, 9))
    mplt.bar(xAxis,yAxis)
    mplt.yticks(range(max(yAxis) + 1))
    mplt.xticks(xAxis) # Only shows labels for days with tasks completed; otherwise, the bars and dates won't align cleanly
    mplt.ylabel('Tasks Completed')
    mplt.xlabel('Deadline Day')

    # Make BytesIO virtual file
    vFileBuffer = BytesIO()
    mplt.savefig(vFileBuffer, format='png')
    vFileGraph = vFileBuffer.getvalue()
    vFileBuffer.close()

    # Convert graph and pass to HTML template
    completedGraph = base64.b64encode(vFileGraph).decode('utf-8')

    # Add graph to context
    context['graph'] = completedGraph

    return render(request, 'calendar_app/graph_completed.html', context)
