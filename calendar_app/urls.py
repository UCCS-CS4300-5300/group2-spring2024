from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, reverse_lazy

from . import views
from .views.account_views import *
from .views.api_views import *
from .views.category_views import *
from .views.display_views import *
from .views.graph_views import *
from .views.task_views import *

urlpatterns = [
    path('', index, name='index'),
    path('', index, name='index'),
    path('home/', index, name='home'),


    # category CRUD
    path('category/create', createCategory, name='create-category'),
    path('category/update/<int:category_id>',
         updateCategory, name='update-category'),
    path('category/delete/<int:category_id>',
         deleteCategory, name='delete-category'),
    path('category/list', CategoryListView.as_view(), name='category-list'),

    path('task/create', createTask, name='create-task'),
    path('task/update/<int:task_id>', updateTask, name='update-task'),
    path('task/delete/<int:task_id>', deleteTask, name='delete-task'),
    path('task/', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='task-detail'),

    ###########################################################
    path('register/', register, name='register'),
    # After user registers this sends them to the homepage
    path('home/', index, name='home'),
    path('register/home/', index, name='index'),
    path('login/', LoginView.as_view(template_name='calendar_app/accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    ###########################################################

    # WeekView
    # Default path for the current week with optional category filtering
    path('calendar/week/', week_view,
         {'category_str': None, 'year': None, 'month': None, 'day': None}, name='week-view'),
    path('calendar/week/filter/<str:category_str>/', week_view,
         {'year': None, 'month': None, 'day': None}, name='filtered-week-view'),

    # Paths for navigating to specific weeks, with and without category filtering
    path('calendar/week/<int:year>/<int:month>/<int:day>/',
         week_view, {'category_str': None}, name='week-view-date'),
    path('calendar/week/filter/<str:category_str>/<int:year>/<int:month>/<int:day>/',
         week_view, name='filtered-week-view-date'),


    # MonthView
    path('calendar/month/', MonthView.as_view(),
         {'category_str': None}, name='month-view'),
    path('calendar/month/filter/<str:category_str>/',
         MonthView.as_view(), name='filtered-month-view'),
    # path('calendar/month/filter/<int:category>',MonthView.as_view(),name='filtered-month-view')

    # Monthly graphs
    path('graph/completed/month/', graphMonthlyTasksCompleted,
         name='graph-monthly-tasks-completed'),
    path('graph/progress/month/', graphMonthlyTaskProgress,
         name='graph-monthly-task-complete-vs-incomplete'),

    # Google Calendar Imports
    path('import-google-events/', import_google_calendar_events,
         name='import-google-events'),
]
