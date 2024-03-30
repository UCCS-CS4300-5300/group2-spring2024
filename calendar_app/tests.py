from datetime import date, time, timedelta
from datetime import date, time, timedelta, timezone
from django.urls import reverse
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

    def testRegistrationPageLoads(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/accounts/register.html')

class LoginPageTest(TestCase):
    def setUp(self):
        # Set up a user for testing login
        self.CustomUser = CustomUser.objects.create_user(username='testuser', password='1234567!@#$%^&')
        self.CustomUser.save()

    def testLoginViewSuccess(self):
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

# Task View test
class TaskViewTest(TestCase):
    def testTaskPage(self):
        url = reverse('create-task')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/task_form.html')
    # """ def test_email_field_not_blank(self):
    #     # Attempt to create a user without an email
    #     with self.assertRaises(ValueError) as raised:
    #         CustomUser.objects.create_user(username="testuser3", email=None, password="testpassword789")
    #     self.assertEqual(ValueError, type(raised.exception)) """

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


    def test_email_field_not_blank(self):
        # Attempt to create a user without an email
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(username="testuser3", email="", password="testpassword789")


class TasksTests(TestCase):
    # User and Task for Testing CRUD operations
    def setUp(self):
        email = "test@example.com"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")
        # Make tasks
        self.newTask = Task.objects.create(name='TestTask1', description='TestDesc1',
                                           deadlineDay=date(2024, 3, 12), deadlineTime=time(23, 59),
                                           category=None, duration=timedelta(days=0, hours=2),
                                           user=self.customUser, status=False)
    # Test Task creation
    def test_task_creation(self):
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get(id=self.newTask.id).name, 'TestTask1')

    # Test Task details read
    def test_task_details(self):
        response = self.client.get(reverse('task-detail', args=[self.newTask.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTask1')

    # Test Task update
    def test_task_update(self):
        updated_data = {
            'name': 'Updated Test Task',
            'description': 'This is an updated test task',
            'deadlineDay': '2024-03-22',
            'deadlineTime': '13:00:00',
            'status': True
        }
        self.client.force_login(self.customUser)
        response = self.client.post(reverse('update-task', args=[self.newTask.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.newTask.refresh_from_db()
        self.assertEqual(self.newTask.name, 'TestTask1')

    # Test Task deletion
    def test_task_deletion(self):
        self.client.force_login(self.customUser)
        response = self.client.post(reverse('delete-task', args=[self.newTask.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
