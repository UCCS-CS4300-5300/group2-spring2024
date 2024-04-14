from django.shortcuts import render
from ..models import Task
from datetime import datetime

#from django.views import View
from django.db.models import Count

import matplotlib
matplotlib.use('Agg') # Prevent matplotlib runtimeerror
import matplotlib.pyplot as mplt

import numpy as np

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
    currentMonthName=monthNames[int(currentMonth) - 1]
    context['monthAndYear'] = f'{currentMonthName} {currentYear}'

    # Set next and previous months
    day = get_date(request.GET.get('month', None))
    context['prevMonth'] = get_prev_month(day)
    context['thisMonth'] = f'month={currentYear}-{currentMonth}'
    context['nextMonth'] = get_next_month(day)

    # Update month if needed
    selectedMonth = request.GET.get('month')
    if selectedMonth:
        currentYear, currentMonth = selectedMonth.split('-')
        currentMonthName=monthNames[int(currentMonth) - 1]
        context['monthAndYear'] = f'{currentMonthName} {currentYear}'
    
    # Get completed (status=True) Task objects
    tasksCompleted = Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear,status=True).values('deadlineDay').annotate(numCompleted=Count('deadlineDay'))

    # Check if there are actually completed tasks
    if tasksCompleted:
        # Create graph with matplotlib
        # Number of tasks on y vs day completed on x
        yAxis = [result['numCompleted'] for result in tasksCompleted]
        xAxis = [result['deadlineDay'] for result in tasksCompleted]

        # Set aspect ratio, margins, axis scale/ticks, and labels
        mplt.figure(figsize=(16, 9))
        mplt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
        mplt.bar(xAxis, yAxis)
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
    else:
        context['noGraph'] = True

    return render(request, 'calendar_app/graph_completed.html', context)

def graphMonthlyTaskProgress(request, year=None, month=None, day=None):
    context = {}

    # Get current date
    currentDate = datetime.today()
    
    # Set current month and year to pass to template for display
    monthNames = ["January", "February", "March", "April", "May", "June", "July", 
                  "August", "September", "October", "November", "December"]
    currentYear = currentDate.year
    currentMonth = currentDate.month
    currentMonthName=monthNames[int(currentMonth) - 1]
    context['monthAndYear'] = f'{currentMonthName} {currentYear}'

    # Set next and previous months
    day = get_date(request.GET.get('month', None))
    context['prevMonth'] = get_prev_month(day)
    context['thisMonth'] = f'month={currentYear}-{currentMonth}'
    context['nextMonth'] = get_next_month(day)

    # Update month if needed
    selectedMonth = request.GET.get('month')
    if selectedMonth:
        currentYear, currentMonth = selectedMonth.split('-')
        currentMonthName=monthNames[int(currentMonth) - 1]
        context['monthAndYear'] = f'{currentMonthName} {currentYear}'
    
    # Check if there are Tasks in the month
    tasks = Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear)

    # Check if there are actually completed tasks
    if tasks:
        # Get total, complete (status=True), and incomplete (status=False) Task objects
        tasksTotal =  Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear).values('deadlineDay').annotate(numTotal=Count('deadlineDay'))
        tasksIncomplete = Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear,status=False).values('deadlineDay').annotate(numIncomplete=Count('deadlineDay'))
        tasksComplete = Task.objects.filter(deadlineDay__month=currentMonth,deadlineDay__year=currentYear,status=True).values('deadlineDay').annotate(numComplete=Count('deadlineDay'))

        # Create graph with matplotlib
        # Number of tasks on y vs day completed on x
        yAxisIncomplete = [result['numIncomplete'] for result in tasksIncomplete]
        yAxisComplete = [result['numComplete'] for result in tasksComplete]
        xAxis = [result['deadlineDay'] for result in tasksTotal]

        # Pad if necessary
        if len(yAxisIncomplete) > 0:
            if max(yAxisIncomplete) < len(xAxis):
                yAxisIncomplete = np.pad(yAxisIncomplete, (0, len(xAxis) - len(yAxisIncomplete)), mode='constant', constant_values=0)
            elif max(yAxisIncomplete) > len(xAxis):
                xAxis = np.pad(xAxis, (0, len(yAxisIncomplete) - len(xAxis)), mode='constant', constant_values=0)
        else:
            yAxisIncomplete = np.pad(yAxisIncomplete, (0, len(xAxis) - len(yAxisIncomplete)), mode='constant', constant_values=0)
        if len(yAxisComplete) > 0:
            if max(yAxisComplete) < len(xAxis):
                yAxisComplete = np.pad(yAxisComplete, (0, len(xAxis) - len(yAxisComplete)), mode='constant', constant_values=0)
            elif max(yAxisComplete) > len(xAxis):
                xAxis = np.pad(xAxis, (0, len(yAxisComplete) - len(xAxis)), mode='constant', constant_values=0)
        else:
            yAxisComplete = np.pad(yAxisComplete, (0, len(xAxis) - len(yAxisComplete)), mode='constant', constant_values=0)

        # Set highest yAxis
        if len(yAxisIncomplete) > len(yAxisComplete):
            yAxisMax = len(yAxisIncomplete)
        else:
            yAxisMax = len(yAxisComplete)

        # Set aspect ratio, margins, axis scale/ticks, labels, and legend
        mplt.figure(figsize=(16, 9))
        mplt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9)
        mplt.plot(xAxis, yAxisIncomplete, marker='o', color='r', linestyle='-', label='Incomplete Tasks')
        mplt.plot(xAxis, yAxisComplete, marker='o', color='b', linestyle='-', label='Complete Tasks')
        mplt.yticks(range(yAxisMax + 1))
        mplt.xticks(xAxis) # Only shows labels for days with tasks completed; otherwise, the bars and dates won't align cleanly
        mplt.ylabel('Number of Tasks')
        mplt.xlabel('Deadline Day')
        mplt.legend()

        # Make BytesIO virtual file
        vFileBuffer = BytesIO()
        mplt.savefig(vFileBuffer, format='png')
        vFileGraph = vFileBuffer.getvalue()
        vFileBuffer.close()

        # Convert graph and pass to HTML template
        completedGraph = base64.b64encode(vFileGraph).decode('utf-8')

        # Add graph to context
        context['graph'] = completedGraph
    else:
        context['noTasks'] = True

    return render(request, 'calendar_app/graph_complete_vs_incomplete.html', context)