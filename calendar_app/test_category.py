import datetime

from django.test import Client, TestCase
from django.urls import reverse

from .models import *
from .views.display_views import serialize_category_list


class CategoryCRUDTestCase(TestCase):
    def setUp(self):
        currentdate = str(datetime.date.today())
        self.user1 = CustomUser.objects.create_user(
            username='testuser', password='password12345', email="test@email.com")
        self.client = Client()
        self.category1 = Category.objects.create(
            name="Category 1", user=self.user1)
        self.category2 = Category.objects.create(
            name="Category 2", user=self.user1)
        self.category3 = Category.objects.create(
            name="Category 3", user=self.user1)
        self.categorizedTask = Task.objects.create(name="Categorized Task", description="ex", deadlineDay=currentdate,
                                                   deadlineTime="10:00:00", duration=datetime.timedelta(days=1),  category=self.category1, status=False, user=self.user1)
        self.uncategorizedTask = Task.objects.create(name="task with no category", description="ex", deadlineDay=currentdate,
                                                     deadlineTime="10:00:00", duration=datetime.timedelta(days=1), status=False, user=self.user1)
        self.category2Task = Task.objects.create(name="Category 2 Task", description="ex", deadlineDay=currentdate,
                                                 deadlineTime="10:00:00", duration=datetime.timedelta(days=1), category=self.category2, status=False, user=self.user1)
        self.category3Task = Task.objects.create(name="Category 3 Task", description="ex", deadlineDay=currentdate,
                                                 deadlineTime="10:00:00", duration=datetime.timedelta(days=1), category=self.category3, status=False, user=self.user1)
        self.client.login(username='testuser', password='password12345')

    def test_categories_created(self):
        categories = Category.objects.all()

        self.assertEquals(len(categories), 3)
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

    def test_category_list_view(self):
        response = self.client.get(reverse('category-list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')
        self.assertContains(response, self.category1.name)
        self.assertContains(response, self.category2.name)

    def test_delete_category(self):
        url = reverse('delete-category', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/delete_category_form.html')
        self.assertContains(response, self.category1.name)

        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Category.objects.count(), 2)
        self.assertNotIn(self.category1, Category.objects.all())

    def test_create_category(self):
        url = reverse('create-category')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/create_category_form.html')

        response = self.client.post(
            url, {'name': 'New Category', 'color': '#000000'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Category.objects.count(), 4)
        self.assertIn(Category.objects.get(
            name='New Category'), Category.objects.all())

    def test_update_category(self):
        url = reverse('update-category', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/update_category_form.html')
        self.assertContains(response, self.category1.name)

        response = self.client.post(
            url, {'name': 'Updated Category', 'color': '#000000'})
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Category.objects.count(), 3)
        self.assertIn(Category.objects.get(
            name='Updated Category'), Category.objects.all())

    def test_category_dropdown_week(self):
        url = reverse('week-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        for category in Category.objects.all():
            self.assertContains(response, category.name)

    def test_category_dropdown_month(self):
        url = reverse('month-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        for category in Category.objects.all():
            self.assertContains(response, category.name)

    def test_category_filtering_week(self):
        url = reverse('filtered-week-view', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertNotContains(response, self.uncategorizedTask.name)

        url = reverse('week-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertContains(response, self.uncategorizedTask.name)

    def test_multi_category_filtering_week(self):
        url = reverse('filtered-week-view',
                      args=[serialize_category_list([self.category1.id, self.category2.id])])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertNotContains(response, self.uncategorizedTask.name)
        self.assertContains(response, self.category2Task.name)
        self.assertNotContains(response, self.category3Task.name)

    def test_multi_category_filtering_month(self):
        url = reverse('filtered-month-view',
                      args=[serialize_category_list([self.category1.id, self.category2.id])])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertNotContains(response, self.uncategorizedTask.name)
        self.assertContains(response, self.category2Task.name)
        self.assertNotContains(response, self.category3Task.name)

    def test_category_filtering_month(self):
        url = reverse('filtered-month-view', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertNotContains(response, self.uncategorizedTask.name)

        url = reverse('month-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.categorizedTask.name)
        self.assertContains(response, self.uncategorizedTask.name)


class CategoryUserFilteringTestCase(TestCase):
    def setUp(self):
        currentdate = str(datetime.date.today())
        self.user1 = CustomUser.objects.create_user(
            username='testuser', password='password12345', email="test@email.com")
        self.user2 = CustomUser.objects.create_user(
            username='testuser2', password='password12345', email="test2@email.com")
        self.client = Client()
        self.user1Category = Category.objects.create(
            name="Category 1", user=self.user1)
        self.user2Category = Category.objects.create(
            name="Category 2", user=self.user2)
        self.user1Task = Task.objects.create(name="Categorized Task", description="ex", deadlineDay=currentdate, deadlineTime="10:00:00",
                                             duration=datetime.timedelta(days=1),  category=self.user1Category, status=False, user=self.user1)
        self.user2Task = Task.objects.create(name="task with no category", description="ex", deadlineDay=currentdate,
                                             deadlineTime="10:00:00", duration=datetime.timedelta(days=1), category=self.user2Category, status=False, user=self.user2)
        self.client.login(username='testuser', password='password12345')

    def test_user_filtering_week(self):
        url = reverse('week-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    def test_user_filtering_month(self):
        url = reverse('month-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    def test_user_filtering_week_category(self):
        url = reverse('filtered-week-view', args=[self.user1Category.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    def test_user_filtering_month_category(self):
        url = reverse('filtered-month-view', args=[self.user1Category.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    def test_user_filtering_category_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')
        self.assertContains(response, self.user1Category.name)
        self.assertNotContains(response, self.user2Category.name)

    def test_user_category_filtering_create_task_form(self):
        response = self.client.get(reverse('create-task'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/task_form.html')

        self.assertContains(response, self.user1Category.name)
        self.assertNotContains(response, self.user2Category.name)

    def test_user_category_filtering_update_task_form(self):
        response = self.client.get(
            reverse('update-task', args=[self.user1Task.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/task_form.html')

        self.assertContains(response, self.user1Category.name)
        self.assertNotContains(response, self.user2Category.name)

    def test_user_category_filtering_task_list(self):
        response = self.client.get(reverse('task-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/task_list.html')

        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    # tests that make sure nothing can be seen/edited if not logged in
    def test_user_filtering_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('week-view'))
        self.assertNotContains(response, self.user1Task.name)

        response = self.client.get(reverse('month-view'))
        self.assertNotContains(response, self.user1Task.name)

    # test that when doing multi category filtering and including
    # a category that the user does not own
    # those tasks are not shown
    def test_multi_category_filtering_week(self):
        url = reverse('filtered-week-view', args=[serialize_category_list(
            [self.user1Category.id, self.user2Category.id])])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/week_view.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)

    def test_multi_category_filtering_month(self):
        url = reverse('filtered-month-view', args=[serialize_category_list(
            [self.user1Category.id, self.user2Category.id])])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar_month.html')
        self.assertContains(response, self.user1Task.name)
        self.assertNotContains(response, self.user2Task.name)


class CategoryUserPermissionsTestCase(TestCase):
    def setUp(self):
        currentdate = str(datetime.date.today())
        self.user1 = CustomUser.objects.create_user(
            username='testuser', password='password12345', email="test@test.com")
        self.user2 = CustomUser.objects.create_user(
            username='testuser2', password='password12345', email="test2@test.com")
        self.client = Client()
        self.user1Category = Category.objects.create(
            name="Category 1", user=self.user1)
        self.user2Category = Category.objects.create(
            name="Category 2", user=self.user2)
        self.user1Task = Task.objects.create(name="Categorized Task", description="ex", deadlineDay=currentdate, deadlineTime="10:00:00",
                                             duration=datetime.timedelta(days=1),  category=self.user1Category, status=False, user=self.user1)
        self.user2Task = Task.objects.create(name="Uncategorized Task", description="ex", deadlineDay=currentdate, deadlineTime="10:00:00",
                                             duration=datetime.timedelta(days=1), category=self.user2Category, status=False, user=self.user2)

    # test that all interactions that need login causes redirect to login page
    def test_login_redirects(self):
        response = self.client.get(reverse('create-category'))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/category/create')

        response = self.client.get(
            reverse('update-category', args=[self.user1Category.id]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, '/login/?next=/category/update/'+str(self.user1Category.id))

        response = self.client.get(
            reverse('delete-category', args=[self.user1Category.id]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(
            response, '/login/?next=/category/delete/'+str(self.user1Category.id))

    def test_permissions_assigned(self):
        self.assertTrue(self.user1.has_perm(
            'view_category', self.user1Category))
        self.assertTrue(self.user1.has_perm(
            'change_category', self.user1Category))
        self.assertTrue(self.user1.has_perm(
            'delete_category', self.user1Category))

        self.assertFalse(self.user1.has_perm(
            'view_category', self.user2Category))
        self.assertFalse(self.user1.has_perm(
            'change_category', self.user2Category))
        self.assertFalse(self.user1.has_perm(
            'delete_category', self.user2Category))

        self.assertTrue(self.user1.has_perm('view_task', self.user1Task))
        self.assertTrue(self.user1.has_perm('change_task', self.user1Task))
        self.assertTrue(self.user1.has_perm('delete_task', self.user1Task))

        self.assertFalse(self.user1.has_perm('view_task', self.user2Task))
        self.assertFalse(self.user1.has_perm('change_task', self.user2Task))
        self.assertFalse(self.user1.has_perm('delete_task', self.user2Task))

    def test_permissions_enforced(self):
        # check can access own categories
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('category-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')
        self.assertContains(response, self.user1Category.name)

        response = self.client.get(reverse('create-category'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/create_category_form.html')

        response = self.client.get(
            reverse('update-category', args=[self.user1Category.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/update_category_form.html')

        response = self.client.get(
            reverse('delete-category', args=[self.user1Category.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'calendar_app/delete_category_form.html')

        # check cannot access other user's categories
        response = self.client.get(reverse('category-list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')
        self.assertNotContains(response, self.user2Category.name)

        response = self.client.get(
            reverse('update-category', args=[self.user2Category.id]))
        self.assertEquals(response.status_code, 403)

        response = self.client.get(
            reverse('delete-category', args=[self.user2Category.id]))
        self.assertEquals(response.status_code, 403)

# CATEGORY LIST VIEW ############################################################

# No categories


class CategoryListNoTasksViewTest(TestCase):
    def setUp(self):
        # Make test user to assign categories to
        email = "testuser@uccs.edu"
        self.user1 = CustomUser.objects.create_user(
            username="testuser", email=email, password="testpassword123")

        self.client.login(username='testuser', password='testpassword123')

    def test_category_list_no_categories_view(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('category-list'))
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')

        # Check for the "no categories" message
        self.assertIn('No categories', response.content.decode())

# With categories


class CategoryListViewTest(TestCase):
    def setUp(self):
        # Make test user to assign categories to
        email = "testuser@uccs.edu"
        self.user1 = CustomUser.objects.create_user(
            username="testuser", email=email, password="testpassword123")

        self.client.login(username='testuser', password='testpassword123')

        # Make categories; colors are arbitrary
        self.category1 = Category.objects.create(
            name="Category 1", user=self.user1, color="#010101")
        self.category2 = Category.objects.create(
            name="Category 2", user=self.user1, color="#aabbcc")
        self.category3 = Category.objects.create(
            name="Category 3", user=self.user1, color="#244224")

    def test_category_list_view(self):
        # Get and verify template being used is correct
        response = self.client.get(reverse('category-list'))
        self.assertTemplateUsed(response, 'calendar_app/category_list.html')

        # Check for index/home and create/add category links
        # Index/home link is present
        self.assertContains(response, reverse('index'))
        # Create/add category link is present
        self.assertContains(response, reverse('create-category'))

        # Check for individual categories in response
        # category1 is present
        self.assertContains(response, self.category1.name)
        # category2 is present
        self.assertContains(response, self.category2.name)
        # category3 is present
        self.assertContains(response, self.category3.name)

        # Check for individual categories' colors in response
        # category1 color is present
        self.assertContains(response, self.category1.color)
        # category2 color is present
        self.assertContains(response, self.category2.color)
        # category3 color is present
        self.assertContains(response, self.category3.color)

        # Check for individual categories' update links in response
        self.assertContains(response, reverse(
            'update-category', args=[self.category1.id]))  # category1 link is present
        self.assertContains(response, reverse(
            'update-category', args=[self.category2.id]))  # category2 link is present
        self.assertContains(response, reverse(
            'update-category', args=[self.category3.id]))  # category3 link is present

        # Check for individual categories' delete links in response
        self.assertContains(response, reverse(
            'delete-category', args=[self.category1.id]))  # category1 link is present
        self.assertContains(response, reverse(
            'delete-category', args=[self.category2.id]))  # category2 link is present
        self.assertContains(response, reverse(
            'delete-category', args=[self.category3.id]))  # category3 link is present
