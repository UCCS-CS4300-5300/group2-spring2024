from datetime import date, time, timedelta
from django.db.utils import IntegrityError
from django.urls import reverse
from django.test import TestCase
from .models import *


# Account creation
class AccountCreationTest(TestCase):
    def test_email_field_unique(self):
        # Create a user with a specific email
        email = "test@example.com"
        CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError) as raised:
            CustomUser.objects.create_user(username="testuser2", email=email, password="testpassword456")

        #have to do this wacky workaround
        self.assertEqual(IntegrityError, type(raised.exception))

    # NICK WILL FIX DO NOT DELETE !!!
    #def test_email_field_not_blank(self):
    #    with self.assertRaises(ValueError) as raised:
    #        CustomUser.objects.create_user(username="testuser3", email="", password="testpassword789")
    #    self.assertIn('The email field cannot be blank.', str(raised.exception))
        
# Login and register view tests
class RegisterPageTest(TestCase):
    def testRegisterView(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '1234567!@#$%^&',
            'password2': '1234567!@#$%^&',
        }
        response = self.client.post(url, data)
        # Check if the registration was successful and redirects as expected
        assert response.status_code == 200  # or 302 

class LoginPageTest(TestCase):
    def setUp(self):
        # Set up a user for testing login
        self.CustomUser = CustomUser.objects.create_user(username='testuser', password='1234567!@#$%^&')
        self.CustomUser.save()

    def test_login_view_success(self):
        # This URL might need to be adjusted if your login route is different.
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': '1234567!@#$%^&',
        }
        response = self.client.post(url, data, follow=True)
        
        # Check if the login was successful and redirects as expected to home page.
        self.assertEqual(response.status_code, 200)
        # Check if authenticated
        self.assertTrue(response.context['user'].is_authenticated)

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


        # Make tasks
        self.newTask = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(2024,3,12),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=False)
        self.newTask = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(2024,3,26),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=1),
                                           user=self.customUser,status=False)
        self.newTask = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(2024,3,30),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=3),
                                           user=self.customUser,status=False)
    
    def test_month_task_display(self):
        # Get and verify template being used is correct
        response = self.client.get('/calendar/month/')
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for individual tasks in response
        self.assertContains(response, 'TestTask1') # TestTask1 is present
        self.assertContains(response, 'TestTask2') # TestTask2 is present
        self.assertContains(response, 'TestTask3') # TestTask3 is present

# Account creation
class AccountCreationTest(TestCase):
    def test_email_field_unique(self):
        # Create a user with a specific email
        email = "test@example.com"
        CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")
        # Attempt to create another user with the same email
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(username="testuser2", email=email, password="testpassword456")


class TasksTests(TestCase):
    # make a task
    task = 0

    # add to database and ensure in database
    def test_task_creation(self):
        pass

    # read task and ensure it is correct in the database and readable
    def test_task_read(self):
        pass
