from typing import Any
from django.shortcuts import render
from .models import *
from django.views import generic
from calendar import HTMLCalendar
from datetime import datetime
from django.utils.safestring import mark_safe

# Create your views here.
def index(request):
    # Render index.html
    return render( request, 'calendar_app/index.html')

# Calendar class; overriding HTMLCalendar
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
            dayHtml += f'<a class="btn btn-primary btn-sm" href="#" role="button">{task.name}</a><br>'
        
        # Add numerical date and tasks to cel
        if currentDay != 0:
            return f'<td><p class="text-end">{currentDay}</p><p>{dayHtml}</p></td>'
        
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

        # Label the day cels
        for day in days:
             weekHeader += '<th scope="col">'
             weekHeader += day
             weekHeader += '</th>'

        # Close the table row
        weekHeader += '</tr>'

        return f'<thead>{weekHeader}</thead>'                  

    # Format month name header
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

        return f'<div class="row text-center">{monthHeader}</div><br>'

    # Format the whole current month
    def formatmonth(self, withyear=True):
        tasks = Task.objects.filter(deadlineDay__year=self.year,deadlineDay__month=self.month)

        # Starting HTML; format the month
        cal = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        
        # Start the HTML table for the weeks and days
        cal += f'<table class="table table-bordered">'
        
        # Format the week header
        cal += f'{self.formatweekheader()}\n'
        
        # Format the days
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, tasks)}\n'
        
        return cal
    
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
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()