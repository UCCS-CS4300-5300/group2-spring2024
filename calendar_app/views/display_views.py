from calendar import monthrange
from datetime import date, datetime, timedelta

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.views import generic

from ..calendar_override import Calendar
from ..forms import *
from ..models import *


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
            return redirect(reverse('index'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'calendar_app/accounts/register.html', {'form': form})

# Week View
def week_view(request, category, year=None, month=None, day=None):
    if year and month and day:
        # Use the provided year, month, day if present
        current_date = datetime(year=year, month=month, day=day)
    else:
        # Default to the current date if no parameters are provided by URL
        current_date = datetime.now()

    # If a catagory is chosen, filter based on it
    if category:
        tasks = Task.objects.filter(category=category)
    else:
        tasks = Task.objects.all()

    context = {}

    context['year'] = current_date.year
    context['month'] = current_date.month
    context['day'] = current_date.day
    # Calculate start and end of currently viewed week
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Add start/end to context
    context['start_of_week'] = start_of_week
    context['end_of_week'] = end_of_week

    # Get tasks in current week
    tasks = tasks.filter(deadlineDay__range=[start_of_week, end_of_week])

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

    # Group tasks by their specific date
    for task in tasks:
        task_day = task.deadlineDay.strftime('%A')
        if task_day in days_tasks:
            days_tasks[task_day].append(task)
            
    context['days_tasks'] = days_tasks

    # Add catagories to context
    context['category_list'] = Category.objects.all()
    context['category_colors'] = get_category_color_dict()

    # Create context variables for navigation
    prev_week = start_of_week - timedelta(weeks=1)
    next_week = start_of_week + timedelta(weeks=1)

    # Construct URLs for the prev and next week buttons
    if category:
        prev_week_url = reverse('filtered-week-view-date', args=[category,prev_week.year, prev_week.month, prev_week.day])
        next_week_url = reverse('filtered-week-view-date', args=[category,next_week.year, next_week.month, next_week.day])
    else:
        prev_week_url = reverse('week-view-date', args=[prev_week.year, prev_week.month, prev_week.day])
        next_week_url = reverse('week-view-date', args=[next_week.year, next_week.month, next_week.day])

    context['prev_week_url'] = prev_week_url
    context['next_week_url'] = next_week_url

    return render(request, 'calendar_app/week_view.html', context)



# MonthView; uses ListView
class MonthView(generic.ListView):
    model = Task
    
    # Override need to use task_list.html as filename
    template_name = 'calendar_app/calendar_month.html'
    
    # Working on getting the current day to be outlined in the calender and week
    # views, -nick
    def formatDay(self, day):
        today = date.today()
        # Current date, this will get filled with a string that will match what is needed to outline in our
        # html
        curDate = str(day) if day != 0 else ""
        # returning the html
        if day == today.day and self.year == today.year and self.month == today.month:
           return f"<td class='today'>{curDate}</td>"
        else:
           return f"<td>{curDate}</td>"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #get the category for the filter
        filter_category = self.kwargs.get('category')
        if filter_category:
            context['filter_category'] = filter_category
        context['category_list'] = Category.objects.all()
        context['category_colors'] = get_category_color_dict()

        # Use the current date for the calendar
        currentDay = get_date(self.request.GET.get('month', None))

        # Instantiate Calendar with current year+date
        cal = Calendar(currentDay.year, currentDay.month, filter_category)
        
        # Set first day to Sunday to match approved sketch
        cal.setfirstweekday(6)

        # Use formatmonth to get Calendar as table
        html_cal = cal.formatmonth(withyear=True)

        today = date.today()
        # we are in the current month
        html_cal = cal.formatmonth(withyear=True)
        
        # Highlighting today's date if we're in the current month
        today = date.today()
        if currentDay.year == today.year and currentDay.month == today.month:
            search_pattern = f'<td><p class="text-end">{today.day}</p><p></p></td>'
            replacement = f'<td class="today"><p class="text-end">{today.day}</p><p></p></td>'
            html_cal = html_cal.replace(search_pattern, replacement, 1)
        # logic to highlight with a task:
        
        context['calendar'] = mark_safe(html_cal)

        # Set current month and year to pass to template for display
        monthNames = ["January", "February", "March", "April", "May", "June", "July", 
                      "August", "September", "October", "November", "December"]
        currentYear=str(currentDay.year)
        currentMonth=monthNames[int(currentDay.month) - 1]
        context['monthAndYear'] = f'{currentMonth} {currentYear}'

        # Set next and previous months
        day = get_date(self.request.GET.get('month', None))
        context['prevMonth'] = get_prev_month(day)
        context['thisMonth'] = f'month={currentYear}-{currentDay.month}'
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

#returns a dict of the background and text color for each category
def get_category_color_dict() -> dict[int, tuple[str, str]]:
    category_list = Category.objects.all()
    category_color_dict = {}
    for category in category_list:
        category_color_dict[category.id] = (category.color, get_text_color(category.color))
    return category_color_dict

#https://stackoverflow.com/a/77647094
#gets what the color of the text should be based on text color based on provided algorithm
def get_text_color(backColor:str) -> str:
    if len(backColor) != 7:
        return "#000000"
    r = float(int(backColor[1:3], 16))
    g = float(int(backColor[3:5], 16))
    b = float(int(backColor[5:7], 16))
    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    if luminance > 0.5:
        return "#000000"
    else:
        return "#ffffff"
    
    