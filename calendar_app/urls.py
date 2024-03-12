from django.urls import path, reverse_lazy, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

    
urlpatterns = [
    #path('', views.index, name='index'),


    #category CRUD
    path('create_category', views.createCategory, name='create_category'),
    path('update_category/<int:category_id>', views.updateCategory, name='update_category'),
    path('delete_category/<int:category_id>', views.deleteCategory, name='delete_category'),

    path('create_task', views.createTask, name='create_task'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),

    path('home/', views.index, name='home'),
    path('register/', views.register, name='index'),

    # After user registers this sends them to the homepage
    # path('register/calendar_app/index.html/', views.index, name='index'),
    path('register/home/', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='calendar_app/accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # WeekView
    path('calendar/week/', views.WeekView,{'category':None}, name='week-view'),
    path('calendar/week/filter/<int:category>', views.WeekView, name='filtered-week-view'),

    # MonthView
    path('calendar/month/', views.MonthView.as_view(), {'category':None},name='month-view'),
    path('calendar/month/filter/<int:category>',views.MonthView.as_view(),name='filtered-month-view')
]
