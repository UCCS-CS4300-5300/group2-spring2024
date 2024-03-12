from .models import *
from .forms import TaskForm, CustomUserCreationForm
from django.views import generic
from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import login
from calendar import HTMLCalendar, monthrange
from datetime import datetime, date, timedelta
from django.utils.safestring import mark_safe
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
            return redirect('calendar_app/accounts/index.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendar_app/accounts/register.html', {'form': form})


# Task Creation view
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

def WeekView(request):
    tasks = Task.objects.all()
    current_date = datetime.now().date()

    start_of_week = current_date - timedelta(days=current_date.weekday())

    # Calculate the end date of the current week
    end_of_week = start_of_week + timedelta(days=6)

    # Create a list to store the dates for each weekday
    weekday_dates = []
    for i in range(7):
        weekday_dates.append(start_of_week + timedelta(days=i))

    # Dictionary of day names
    days_tasks = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': [],
    }

    # Group tasks by day
    for task in tasks:
        # Get name of deadline day
        day_of_week = task.deadlineDay.strftime('%A')
        days_tasks[day_of_week].append(task)

    return render(request, 'calendar_app/week_view.html', {'days_tasks': days_tasks, 'start_of_week': start_of_week, 'end_of_week': end_of_week, 'weekday_dates': weekday_dates})

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

# Calendar class for MonthView; overriding HTMLCalendar
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # Format days and filter tasks by day
    # Use bootstrap; display tasks as small buttons
    def formatday(self, currentDay, tasks):
        tasksInDay = tasks.filter(deadlineDay__day=currentDay)
        dayHtml = ''
        
        # Show tasks as small buttons in primary (color)
        for task in tasksInDay:
            taskURL = '#' # Replace with actual task URL later
            dayHtml += f'<a class="btn btn-primary btn-sm w-100" href="{taskURL}" role="button">{task.name}</a><br>'
        
        # Add numerical date and tasks to cell
        if currentDay != 0:
            return f'<td class="text-nowrap"><p class="text-end">{currentDay}</p><p>{dayHtml}</p></td>'
        
        # Return empty otherwise
        return '<td></td>'

    # Format weeks as table rows
    def formatweek(self, currentWeek, tasks):
        weekHtml = ''

        for dayHtml, weekDay in currentWeek:
            weekHtml += self.formatday(dayHtml, tasks)

        return f'<tr>{weekHtml}</tr>'

    # Format weekdays as only the first letter,
    # according to the sketch approved by the customers
    def formatweekheader(self):
        # The first day is Sunday to match the approved sketch
        days = ['S','M','T','W','T','F','S']
        
        # Start the HTML table row
        weekHeader = '<tr class="text-center">'

        # Label the day cells
        for day in days:
             weekHeader += '<th scope="col">'
             weekHeader += day
             weekHeader += '</th>'

        # Close the table row
        weekHeader += '</tr>'

        return f'<thead>{weekHeader}</thead>'                  

    # Format month name header
    # Kept just in case; moved to calendar_month.html with
    # modifications to get_context_data() in MonthView
    '''
    def formatmonthname(self,currentYear,currentMonth,withyear=True):
        monthNames = ["Jan", "Feb", "March", "April", "May", "June", "July", 
                      "August", "September", "October", "November", "December"]
        currentYear=str(currentYear)
        currentMonth=monthNames[currentMonth - 1]
        monthHeader = ''

        # Left arrow button HTML opening div and a/hyperlink 
        # Link needs to be changed later to lead to PREVIOUS month
        monthHeader += '<div class="col-1"><a class="btn btn-primary btn-sm" href="#" role="button">'
        # SVG for left arrow 
        monthHeader += '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/></svg>'
        # Closing div and a/hyperlink tags
        monthHeader += '</a></div>'

        # Month name and year
        monthHeader += '<div class="col-10"><h2>'
        monthHeader += currentMonth
        monthHeader += " " + currentYear
        monthHeader += '</h2></div>'

        # Right arrow button HTML opening div and a/hyperlink 
        # Link needs to be changed later to lead to NEXT month
        monthHeader += '<div class="col-1"><a class="btn btn-primary btn-sm" href="#" role="button">'
        # SVG for right arrow
        monthHeader += '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/></svg>'
        # Closing div and a/hyperlink tags
        monthHeader += '</a></div>'

        return f'<div class="row text-center">{monthHeader}</div>'
    '''

    # Format the whole current month
    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(deadlineDay__year=self.year,deadlineDay__month=self.month)
        cal = ''

        # Starting HTML; format the month
        #cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        # Month name/header is now in calendar_month.html because
        # the buttons to get the next and previous months don't 
        # work from here due to complications with string formatting

        # Start the HTML table for the weeks and days
        cal += f'<table class="table table-bordered table-fixed">'
        
        # Format the week header
        cal += f'{self.formatweekheader()}\n'
        
        # Format the days
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        
        return cal

# MonthView; uses ListView
class MonthView(generic.ListView):
    model = Task

    # Override need to use task_list.html as filename
    template_name = 'calendar_app/calendar_month.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use the current date for the calendar
        currentDay = get_date(self.request.GET.get('day', None))

        # Instantiate Calendar with current year+date
        cal = Calendar(currentDay.year, currentDay.month)
        
        # Set first day to Sunday to match approved sketch
        cal.setfirstweekday(6)

        # Use formatmonth to get Calendar as table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # Set current month and year to pass to template for display
        monthNames = ["Jan", "Feb", "March", "April", "May", "June", "July", 
                      "August", "September", "October", "November", "December"]
        currentYear=str(currentDay.year)
        currentMonth=monthNames[int(currentDay.month) - 1]
        context['monthAndYear'] = f'{currentMonth} {currentYear}'

        # Set next and previous months
        day = get_date(self.request.GET.get('month', None))
        context['prevMonth'] = get_prev_month(day)
        context['nextMonth'] = get_next_month(day)

        return context

# For use with MonthView
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

# For use with MonthView
def get_prev_month(day):
    # Get the starting day
    first = day.replace(day=1)

    # Go back a day to the previous month
    prevMonth = first - timedelta(days=1)

    # Set the new month and year as YYYY-MM
    month = 'month=' + str(prevMonth.year) + '-' + str(prevMonth.month)
    return month

# For use with MonthView
def get_next_month(day):
    # Go to the last day in the month
    days_in_month = monthrange(day.year, day.month)[1]
    last = day.replace(day=days_in_month)
    
    # Go forward a day to the next month
    next_month = last + timedelta(days=1)

    # Set the new month and year as YYYY-MM
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
