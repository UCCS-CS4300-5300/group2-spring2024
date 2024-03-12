from calendar import monthrange
from datetime import date, datetime, timedelta

from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic

from .calendar_override import Calendar
from .forms import *
from .models import *


# Create your views here.
def index(request):
    return redirect('month-view')


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



class TaskDetailView(generic.DetailView):
    model = Task

class TaskListView(generic.ListView):
    model = Task

class CategoryListView(generic.ListView):
    model = Category


def WeekView(request,category):
    if category:
        tasks = Task.objects.filter(category=category)
    else:
        tasks = Task.objects.all()
    current_date = datetime.now().date()

    context = {}

    start_of_week = current_date - timedelta(days=current_date.weekday())
    
    context['start_of_week'] = start_of_week
    # Calculate the end date of the current week
    context['end_of_week'] = start_of_week + timedelta(days=6)

    # Create a list to store the dates for each weekday
    weekday_dates = []
    for i in range(7):
        weekday_dates.append(start_of_week + timedelta(days=i))

    context['weekday_dates'] = weekday_dates
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

    context['days_tasks'] = days_tasks

    context['category_list'] = Category.objects.all()
    return render(request, 'calendar_app/week_view.html', context)



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


def createCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            task = form.save()
            return redirect('index')
    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'calendar_app/generic_form.html', context)

def updateCategory(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    form = CategoryForm(instance=category)
    if request.method == 'POST':
         form = CategoryForm(request.POST, instance=category)
         if form.is_valid():
             form.save()
         return redirect(request.META['HTTP_REFERER'])

    context = {'form': form}
    return render(request, 'calendar_app/task_form.html', context)

def deleteCategory(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    if request.method == 'POST':
       category.delete()
       return redirect('index')
    context = {'category':category}
    return render(request, 'calendar_app/delete_category_form.html', context)
        
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
#         return redirect('index')
#
#     context = {'task': task}
#     return render(request, 'calendar_app/delete_task_form.html', context)

# MonthView; uses ListView
class MonthView(generic.ListView):
    model = Task
    
    # Override need to use task_list.html as filename
    template_name = 'calendar_app/calendar_month.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #get the category for the filter
        filter_category = self.kwargs.get('category')
        context['category_list'] = Category.objects.all()

        # Use the current date for the calendar
        currentDay = get_date(self.request.GET.get('day', None))

        # Instantiate Calendar with current year+date
        cal = Calendar(currentDay.year, currentDay.month,filter_category)
        
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
