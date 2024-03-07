from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('calendar/week/', views.WeekView, name='week-view')
]