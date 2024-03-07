from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.exampleView, name='example-view'),
    path('', views.index, name='index'),

    path('calendar/week/', views.WeekView, name='week-view')
]