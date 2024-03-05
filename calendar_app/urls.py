from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='home'),
    path('register/calendar_app/index.html', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='calendar_app/login.html'), name='login'),
]