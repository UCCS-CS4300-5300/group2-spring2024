import datetime

from django.test import Client, TestCase
from django.urls import reverse

from .models import *


class TaskPermissionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.task = Task.objects.create(name='testtask', user=self.user, category=None, deadlineDay=datetime.date.today())
        self.task2 = Task.objects.create(name='testtask2', user=self.user2, category=None, deadlineDay=datetime.date.today())

    def test_login_redirects(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('create-task'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('update-task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('delete-task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_permissions_assigned(self):
        self.assertTrue(self.user.has_perm('view_task', self.task))
        self.assertTrue(self.user.has_perm('change_task', self.task))
        self.assertTrue(self.user.has_perm('delete_task', self.task))
        self.assertTrue(self.user2.has_perm('view_task', self.task2))
        self.assertTrue(self.user2.has_perm('change_task', self.task2))
        self.assertTrue(self.user2.has_perm('delete_task', self.task2))


    def test_task_detail_view_permission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('task-detail', args=[self.task2.id]))
        self.assertEqual(response.status_code, 403)

    def test_task_month_view_permission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('month-view'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)

        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('month-view'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, self.task.name)
        self.assertContains(response, self.task2.name)

    def test_task_week_view_permission(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('week-view'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)

        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('week-view'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, self.task.name)
        self.assertContains(response, self.task2.name)

    def test_task_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.task.name)
        self.assertNotContains(response, self.task2.name)

        self.client.login(username='testuser2', password='12345')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, self.task.name)
        self.assertContains(response, self.task2.name)


    
        
