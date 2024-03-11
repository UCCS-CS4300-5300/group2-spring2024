from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from datetime import date, time

# Index view template unit test
class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/index.html')

# Month view template unit test
class MonthViewTest(TestCase):
    def test_month_view(self):
        response = self.client.get('/calendar/month/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

# Month view task display integration test
'''
class MonthTaskDisplay(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='TestCaseUser', password='testpass123')
        self.newCat = Category.objects.create(category=1)
        self.newTask = Task.objects.create(name='TestTask',description='TestDesc',
                                           deadlineDay=date(2024,3,12),deadlineTime=time(23,59),
                                           category=self.newCat,duration=3,
                                           user=self.user,status=False)
    
    def test_month_task_display(self):
        response = self.client.get('/calendar/month/')
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, 'TestTask') # Task is present
'''