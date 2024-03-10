from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/month/', views.MonthView.as_view(), name='month-view'),
]