from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    # Task CRUD
    # Both the following require /<int:pk> onto the url for task id
    #path('update_task\<int:pk>', views.updateTask, name='update_task'),
    #path('delete_task\<int:pk>', views.deleteTask, name='delete_task'),
    # path('tasks/', views.TaskListView.as_view(), name='task-list'),
    # path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),

    #category CRUD
    path('create_category', views.createCategory, name='create_category'),
    path('update_category/<int:category_id>', views.updateCategory, name='update_category'),
    path('delete_category/<int:category_id>', views.deleteCategory, name='delete_category'),

    path('home/', views.index, name='home'),
    path('register/', views.register, name='index'),

    # After user registers this sends them to the homepage
    # path('register/calendar_app/index.html/', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='calendar_app/accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Task CRUD URLs
    path('create_task', views.createTask, name='create_task'),

    # WeekView
    path('calendar/week/', views.WeekView, name='week-view'),

    # MonthView
    path('calendar/month/', views.MonthView.as_view(), name='month-view'),
]
