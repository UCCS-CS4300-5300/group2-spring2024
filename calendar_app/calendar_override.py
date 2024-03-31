from calendar import HTMLCalendar

from .models import Task

from django.urls import reverse

# Calendar class; overriding HTMLCalendar
class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None,filter_category=None):
        self.year = year
        self.month = month
        self.filter_category = filter_category
        super(Calendar, self).__init__()

    # Format days and filter tasks by day
    # Use bootstrap; display tasks as small buttons
    def formatday(self, currentDay, tasks,filter_category):
        if filter_category:
            tasksInDay = tasks.filter(deadlineDay__day=currentDay,category=filter_category)
        else:
            tasksInDay = tasks.filter(deadlineDay__day=currentDay)
        dayHtml = ''
        
        # Show tasks as small buttons in primary (color)
        for task in tasksInDay:
            taskURL = reverse('task-detail', args=[task.id])
            colorClass = "btn-primary"
            if task.category:
                colorClass = f"category-{task.category.id}"
            dayHtml += f'<a class="btn {colorClass} btn-sm w-100" href="{taskURL}" role="button">{task.name}</a><br>'
        
        # Add numerical date and tasks to cell
        if currentDay != 0:
            return f'<td class="text-nowrap"><p class="text-end">{currentDay}</p><p>{dayHtml}</p></td>'
        
        # Return empty otherwise
        return '<td></td>'

    # Format weeks as table rows
    def formatweek(self, currentWeek, tasks,filter_category):
        weekHtml = ''

        for dayHtml, weekDay in currentWeek:
            weekHtml += self.formatday(dayHtml, tasks,filter_category)

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
        monthNames = ["January", "February", "March", "April", "May", "June", "July", 
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
            cal += f'{self.formatweek(week, tasks,self.filter_category)}\n'
        
        return cal
