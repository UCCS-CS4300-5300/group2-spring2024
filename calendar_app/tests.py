from datetime import date, datetime, time, timedelta, timezone

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string

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

#############################################################################
# Month view tests
#############################################################################

# Month view template test
# Modified to check current month
class MonthViewTest(TestCase):
    def test_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the current year, month, and month name
        currYear = currMonthDate.year
        currMonth = currMonthDate.month
        currMonthName = months[currMonth-1] # Indices start at 0

        # Check URL, response status, and template
        response = self.client.get(reverse('month-view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for correct year and month
        self.assertContains(response, currYear)
        self.assertContains(response, currMonthName)

# Next view template test
# Modified version of MonthViewTest
class NextMonthViewTest(TestCase):
    def test_next_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)

        # Get the current year, month, and month name
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month
        nextMonthName = months[nextMonth-1] # Indices start at 0

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('month-view')+f'?month={nextYear}-{nextMonth}' 

        # Check URL, response status, and template
        response = self.client.get(nextMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for correct year and month
        self.assertContains(response, nextYear)
        self.assertContains(response, nextMonthName)

# Previous view template test
# Modified version of MonthViewTest
class PrevMonthViewTest(TestCase):
    def test_prev_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year, month, and month name
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month
        prevMonthName = months[prevMonth-1] # Indices start at 0

        # Previous month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('month-view')+f'?month={prevYear}-{prevMonth}' 

        # Check URL, response status, and template
        response = self.client.get(prevMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for correct year and month
        self.assertContains(response, prevYear)
        self.assertContains(response, prevMonthName)

# Month view task display integration test
class MonthTaskDisplay(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Make tasks in current month; days are arbitrary
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,4),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=False)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,16),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=1),
                                           user=self.customUser,status=False)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,28),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=3),
                                           user=self.customUser,status=False)

    def test_month_task_display(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('month-view'))
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for individual tasks in response
        self.assertContains(response, self.newTask1.name) # TestTask1 is present
        self.assertContains(response, self.newTask2.name) # TestTask2 is present
        self.assertContains(response, self.newTask3.name) # TestTask3 is present

        # Check for individual tasks' detail links in response
        self.assertContains(response, reverse('task-detail', args=[self.newTask1.id])) # TestTask1 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask2.id])) # TestTask2 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask3.id])) # TestTask3 link is present

# Test for tasks in next month in month view;
# modified version of MonthTaskDisplay
class NextMonthTaskDisplay(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)
        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)

        # Make next month tasks; days are arbitrary
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=False)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=False)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=False)
    
    def test_next_month_task_display(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)
        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('month-view')+f'?month={nextMonthDate.year}-{nextMonthDate.month}'
        
        # Get and verify template being used is correct
        response = self.client.get(nextMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for individual tasks in response
        self.assertContains(response, self.newTask1.name) # TestTask1 is present
        self.assertContains(response, self.newTask2.name) # TestTask2 is present
        self.assertContains(response, self.newTask3.name) # TestTask3 is present

        # Check for individual tasks' detail links in response
        self.assertContains(response, reverse('task-detail', args=[self.newTask1.id])) # TestTask1 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask2.id])) # TestTask2 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask3.id])) # TestTask3 link is present

# Test for tasks in previous month in month view;
# modified version of MonthTaskDisplay
class PrevMonthTaskDisplay(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)
        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Make previous month tasks; days are arbitrary
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,6),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=False)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,15),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=False)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,25),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=False)
    
    def test_prev_month_task_display(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)
        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('month-view')+f'?month={prevMonthDate.year}-{prevMonthDate.month}'
        
        # Get and verify template being used is correct
        response = self.client.get(prevMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')

        # Check for individual tasks in response
        self.assertContains(response, self.newTask1.name) # TestTask1 is present
        self.assertContains(response, self.newTask2.name) # TestTask2 is present
        self.assertContains(response, self.newTask3.name) # TestTask3 is present

        # Check for individual tasks' detail links in response
        self.assertContains(response, reverse('task-detail', args=[self.newTask1.id])) # TestTask1 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask2.id])) # TestTask2 link is present
        self.assertContains(response, reverse('task-detail', args=[self.newTask3.id])) # TestTask3 link is present

#############################################################################
# End of month view tests
#############################################################################

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

class WeekTest(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser", email=email, password="testpassword123")

        # Get the current day
        currentDay = datetime.now().date()
        

        # Make test tasks in current week
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(currentDay.year, currentDay.month, currentDay.day),deadlineTime=time(12,0),
                                           category=None,duration=timedelta(hours=1),
                                           user=self.customUser,status=False)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(currentDay.year, currentDay.month, currentDay.day),deadlineTime=time(0,1),
                                           category=None,duration=timedelta(hours=2),
                                           user=self.customUser,status=False)

    def test_week_task_display(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('week-view'))
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')

        # Check that tasks exist
        self.assertContains(response, self.newTask1.name)
        self.assertContains(response, self.newTask2.name)

        # Check URLs for task detail views
        self.assertContains(response, reverse('task-detail', args=[self.newTask1.id]))
        self.assertContains(response, reverse('task-detail', args=[self.newTask2.id]))

class TestCurrentDay(TestCase):
    def testDateHtmlGenerationMonth(self):
        response = self.client.get(reverse('month-view'))
        self.assertEqual(response.status_code, 200)

        # Get today's date in the format that matches the HTML output
        today_date = datetime.now().day

        # Construct the HTML snippet for today's date
        expected_html = f'<td class="today"><p class="text-end">{today_date}</p><p></p></td>'

        # Check if the expected HTML snippet is in the response content
        self.assertIn(expected_html, response.content.decode('utf-8'))

    def testDateHtmlGenerationWeek(self):
        response = self.client.get(reverse('week-view')) 
        self.assertEqual(response.status_code, 200)

        today_date = datetime.now().day

        # This checks for the class "today" but not for the tasks or button structure
        self.assertTrue('class="col-1 today"' in response.content.decode('utf-8'))

#############################################################################
# Graph tests (Completed tasks) #############################################
#############################################################################
        
# TEMPLATE TESTS ############################################################
        
# Current month view template test
class GraphCompletedMonthViewTest(TestCase):
    def test_graph_completed_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the current year, month, and month name
        currYear = currMonthDate.year
        currMonth = currMonthDate.month
        currMonthName = months[currMonth-1] # Indices start at 0

        # Check URL, response status, and template
        response = self.client.get(reverse('graph-monthly-tasks-completed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for correct year and month
        self.assertContains(response, currYear)
        self.assertContains(response, currMonthName)

# Next view template test
# Modified version of GraphCompletedMonthViewTest
class GraphCompletedNextMonthViewTest(TestCase):
    def test_graph_completed_next_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)

        # Get the current year, month, and month name
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month
        nextMonthName = months[nextMonth-1] # Indices start at 0

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={nextYear}-{nextMonth}' 

        # Check URL, response status, and template
        response = self.client.get(nextMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for correct year and month
        self.assertContains(response, nextYear)
        self.assertContains(response, nextMonthName)

# Previous view template test
# Modified version of GraphCompletedMonthViewTest
class GraphCompletedPrevMonthViewTest(TestCase):
    def test_graph_completed_prev_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year, month, and month name
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month
        prevMonthName = months[prevMonth-1] # Indices start at 0

        # Previous month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={prevYear}-{prevMonth}' 

        # Check URL, response status, and template
        response = self.client.get(prevMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for correct year and month
        self.assertContains(response, prevYear)
        self.assertContains(response, prevMonthName)

# NO TASKS TESTS ############################################################

# Test for if there are NO tasks in current month
class GraphCompletedNoTasksTest(TestCase):
    def test_graph_completed_no_tasks(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('graph-monthly-tasks-completed'))
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for the "no completed tasks" message
        self.assertIn('no completed tasks', response.content.decode())

# Test for if there are NO tasks in next month
class GraphCompletedNoTasksNextMonthTest(TestCase):
    def test_graph_completed_next_month_no_tasks(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year and month
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={nextYear}-{nextMonth}' 

        # Get and verify template being used is correct
        response = self.client.get(nextMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for the "no completed tasks" message
        self.assertIn('no completed tasks', response.content.decode())

# Test for if there are NO tasks in prev month
class GraphCompletedNoTasksPrevMonthTest(TestCase):
    def test_graph_completed_prev_month_no_tasks(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year and month
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month

        # Previous month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={prevYear}-{prevMonth}' 
        
        # Get and verify template being used is correct
        response = self.client.get(prevMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for the "no completed tasks" message
        self.assertIn('no completed tasks', response.content.decode())

# GRAPH GENERATION TESTS ####################################################

# Current month graph generation test
class GraphCompletedBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Make next month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_completed_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('graph-monthly-tasks-completed'))
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

# Next month graph generation test
class GraphCompletedNextMonthBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next year and month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month

        # Next month URL; argument is the same as used in
        # the graph_completed.html template
        self.nextMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={nextYear}-{nextMonth}' 

        # Make next month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_completed_next_month_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(self.nextMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

# Prev month graph generation test
class GraphCompletedPrevMonthBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous year and month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month

        # Previous month URL; argument is the same as used in
        # the graph_completed.html template
        self.prevMonthURL = reverse('graph-monthly-tasks-completed')+f'?month={prevYear}-{prevMonth}' 

        # Make previous month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_completed_prev_month_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(self.prevMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_completed.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

#############################################################################
# End of graph tests (Completed tasks) ######################################
#############################################################################     
        
#############################################################################
# Graph tests (Complete vs incomplete tasks) ################################
#############################################################################

# TEMPLATE TESTS ############################################################

# Current month view template test
class GraphProgressMonthViewTest(TestCase):
    def test_graph_progress_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the current year, month, and month name
        currYear = currMonthDate.year
        currMonth = currMonthDate.month
        currMonthName = months[currMonth-1] # Indices start at 0

        # Check URL, response status, and template
        response = self.client.get(reverse('graph-monthly-task-complete-vs-incomplete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for correct year and month
        self.assertContains(response, currYear)
        self.assertContains(response, currMonthName)

# Next view template test
# Modified version of GraphProgressMonthViewTest
class GraphProgressNextMonthViewTest(TestCase):
    def test_graph_progress_next_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)

        # Get the next year, month, and month name
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month
        nextMonthName = months[nextMonth-1] # Indices start at 0

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={nextYear}-{nextMonth}' 

        # Check URL, response status, and template
        response = self.client.get(nextMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for correct year and month
        self.assertContains(response, nextYear)
        self.assertContains(response, nextMonthName)

# Previous view template test
# Modified version of GraphProgressMonthViewTest
class GraphProgressPrevMonthViewTest(TestCase):
    def test_graph_progress_prev_month_view(self):
        # List of month names
        months = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December',]
        
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year, month, and month name
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month
        prevMonthName = months[prevMonth-1] # Indices start at 0

        # Previous month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={prevYear}-{prevMonth}' 

        # Check URL, response status, and template
        response = self.client.get(prevMonthURL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for correct year and month
        self.assertContains(response, prevYear)
        self.assertContains(response, prevMonthName)

# GRAPH GENERATION TESTS ####################################################

# Test for if there are NO tasks in current month
class GraphProgressNoTasksTest(TestCase):
    def test_graph_progress_no_tasks(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('graph-monthly-task-complete-vs-incomplete'))
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for the "no tasks" message
        self.assertIn('no tasks', response.content.decode())

# Test for if there are NO tasks in next month
class GraphProgressNoTasksNextMonthTest(TestCase):
    def test_graph_progress_next_month_no_tasks(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year and month
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month

        # Next month URL; argument is the same as used in
        # the calendar_month.html template
        nextMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={nextYear}-{nextMonth}' 
        
        # Get and verify template being used is correct
        response = self.client.get(nextMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for the "no tasks" message
        self.assertIn('no tasks', response.content.decode())

# Test for if there are NO tasks in prev month
class GraphProgressNoTasksPrevMonthTest(TestCase):
    def test_graph_progress_prev_month_no_tasks(self):
        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)

        # Get the current year and month
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month

        # Previous month URL; argument is the same as used in
        # the calendar_month.html template
        prevMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={prevYear}-{prevMonth}' 
        
        # Get and verify template being used is correct
        response = self.client.get(prevMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for the "no tasks" message
        self.assertIn('no tasks', response.content.decode())

# GRAPH GENERATION TESTS ####################################################

# Current month graph generation test
class GraphProgressBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Make next month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(currMonthDate.year,currMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_progress_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('graph-monthly-task-complete-vs-incomplete'))
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

# Next month graph generation test
class GraphProgressNextMonthBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the next year and month
        nextMonthDate = currMonthDate.replace(month=currMonthDate.month+1)
        nextYear = nextMonthDate.year
        nextMonth = nextMonthDate.month

        # Next month URL; argument is the same as used in
        # the graph_completed.html template
        self.nextMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={nextYear}-{nextMonth}' 

        # Make next month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(nextMonthDate.year,nextMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_progress_next_month_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(self.nextMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

# Prev month graph generation test
class GraphProgressPrevMonthBase64Test(TestCase):
    def setUp(self):
        # Make test user to assign tasks to
        email = "testuser@uccs.edu"
        self.customUser = CustomUser.objects.create_user(username="testuser1", email=email, password="testpassword123")

        # Get the first day of the current month
        currMonthDate = datetime.now().replace(day=1)

        # Get the previous year and month
        prevMonthDate = currMonthDate.replace(month=currMonthDate.month-1)
        prevYear = prevMonthDate.year
        prevMonth = prevMonthDate.month

        # Previous month URL; argument is the same as used in
        # the graph_completed.html template
        self.prevMonthURL = reverse('graph-monthly-task-complete-vs-incomplete')+f'?month={prevYear}-{prevMonth}' 

        # Make previous month tasks; days are arbitrary
        # 3 completed
        self.newTask1 = Task.objects.create(name='TestTask1',description='TestDesc1',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,2),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=4),
                                           user=self.customUser,status=True)
        self.newTask2 = Task.objects.create(name='TestTask2',description='TestDesc2',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,8),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=2),
                                           user=self.customUser,status=True)
        self.newTask3 = Task.objects.create(name='TestTask3',description='TestDesc3',
                                           deadlineDay=date(prevMonthDate.year,prevMonthDate.month,24),deadlineTime=time(23,59),
                                           category=None,duration=timedelta(days=0, hours=8),
                                           user=self.customUser,status=True)

    def test_graph_progress_prev_month_base64(self):
        # Get and verify template being used is correct
        response = self.client.get(self.prevMonthURL)
        self.assertTemplateUsed(response, 'calendar_app/graph_complete_vs_incomplete.html')

        # Check for base64 string (shouldn't be generated if there are errors or no tasks)
        self.assertIn('data:image/png;base64,', response.content.decode())

#############################################################################
# End of graph tests (Complete vs incomplete tasks) #########################
#############################################################################