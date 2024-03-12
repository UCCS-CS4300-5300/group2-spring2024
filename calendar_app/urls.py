from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

    
urlpatterns = [
    
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('register/', views.register, name='index'),
    # After user registers this sends them to the homepage
    path('register/home/', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='calendar_app/accounts/login.html'), name='login'),
    # Repeated, to try and fix registration redirect
    path('login/', LoginView.as_view(template_name='calendar_app/accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('calendar/week/', views.WeekView, name='week-view'),
    path('create_task', views.createTask, name='create_task'),
    path('calendar/month/', views.MonthView.as_view(), name='month-view'),
]
