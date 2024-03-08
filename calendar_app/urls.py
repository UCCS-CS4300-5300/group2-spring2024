from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_task', views.createTask, name='create_task'),

]
