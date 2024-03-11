from django.test import TestCase
from .models import *
from datetime import date, time, timedelta
from django.db.utils import IntegrityError

# Index view template test
class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/index.html')

# Month view template test
class MonthViewTest(TestCase):
    def test_month_view(self):
        response = self.client.get('/calendar/month/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

# Month view task display integration test
class MonthTaskDisplay(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")
        
        # Categories; category must be unique according to current Task model
        self.newCat = Category.objects.create(category=1)
        self.newCat2 = Category.objects.create(category=2)
        self.newCat3 = Category.objects.create(category=3)

        # Make tasks
        self.newTask = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(2024,3,12),deadlineTime=time(23,59),
                                           category=self.newCat,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=False)
        self.newTask = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(2024,3,26),deadlineTime=time(23,59),
                                           category=self.newCat2,duration=timedelta(days=0, hours=1),
                                           user=self.customUser,status=False)
        self.newTask = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(2024,3,30),deadlineTime=time(23,59),
                                           category=self.newCat3,duration=timedelta(days=0, hours=3),
                                           user=self.customUser,status=False)
    
    def test_month_task_display(self):
        # Get and verify template being used is correct
        response = self.client.get('/calendar/month/')
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for individual tasks in response
        self.assertContains(response, 'TestTask1') # TestTask1 is present
        self.assertContains(response, 'TestTask2') # TestTask2 is present
        self.assertContains(response, 'TestTask3') # TestTask3 is present