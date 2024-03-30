from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, reverse_lazy
from . import views
from .views.category_views import * 
from .views.display_views import *
from .views.task_views import *
from .views.account_views import *

urlpatterns = [
    path('', index , name='index'),
    path('',index , name='index'),
    path('home/',index , name='home'),


    #category CRUD
    path('category/create', createCategory, name='create-category'),
    path('category/update/<int:category_id>', updateCategory, name='update-category'),
    path('category/delete/<int:category_id>', deleteCategory, name='delete-category'),
    path('category/list',CategoryListView.as_view(),name='category-list'),

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
    path('calendar/week/', WeekView,{'category':None}, name='week-view'),
    path('calendar/week/filter/<int:category>', WeekView, name='filtered-week-view'),

    # MonthView
    path('calendar/month/', MonthView.as_view(), {'category':None},name='month-view'),
    path('calendar/month/filter/<int:category>',MonthView.as_view(),name='filtered-month-view')
]
