import datetime

from django.test import Client, TestCase
from django.urls import reverse

from .models import *


class CategoryCRUDTestCase(TestCase):
    def setUp(self):
        currentdate = str(datetime.date.today())
        self.Client = Client()
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")
        self.categorizedTask = Task.objects.create(name="Categorized Task",description="ex",deadlineDay=currentdate,deadlineTime="10:00:00",duration=datetime.timedelta(days=1),  category=self.category1,status=False)
        self.uncategorizedTask= Task.objects.create(name="Uncategorized Task",description="ex",deadlineDay=currentdate,deadlineTime="10:00:00",duration=datetime.timedelta(days=1),status=False)
    def test_categories_created(self):
        categories = Category.objects.all()

        self.assertEquals(len(categories),2)
        self.assertIn(self.category1,categories)
        self.assertIn(self.category2,categories)

    def test_category_list_view(self):
        response = self.client.get(reverse('category-list'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/category_list.html')
        self.assertContains(response,self.category1.name)
        self.assertContains(response,self.category2.name)

    def test_delete_category(self):
        url = reverse('delete-category',args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/delete_category_form.html')
        self.assertContains(response,self.category1.name)

        response = self.client.post(url)
        self.assertEquals(response.status_code,302)
        self.assertEquals(Category.objects.count(),1)
        self.assertNotIn(self.category1,Category.objects.all())

    def test_create_category(self):
        url = reverse('create-category')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/create_category_form.html')

        response = self.client.post(url,{'name':'New Category','color':'#000000'})
        self.assertEquals(response.status_code,302)
        self.assertEquals(Category.objects.count(),3)
        self.assertIn(Category.objects.get(name='New Category'),Category.objects.all())

    def test_update_category(self):
        url = reverse('update-category',args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/update_category_form.html')
        self.assertContains(response,self.category1.name)

        response = self.client.post(url,{'name':'Updated Category','color':'#000000'})
        self.assertEquals(response.status_code,302)
        self.assertEquals(Category.objects.count(),2)
        self.assertIn(Category.objects.get(name='Updated Category'),Category.objects.all())

    def test_category_dropdown_week(self):
        url = reverse('week-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/week_view.html')
        for category in Category.objects.all():
            self.assertContains(response,category.name)

    def test_category_dropdown_month(self):
        url = reverse('month-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/calendar_month.html')
        for category in Category.objects.all():
            self.assertContains(response,category.name)

    def test_category_filtering_week(self):
        url = reverse('filtered-week-view',args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/week_view.html')
        self.assertContains(response,self.categorizedTask.name)
        self.assertNotContains(response,self.uncategorizedTask.name)

        url = reverse('week-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/week_view.html')
        self.assertContains(response,self.categorizedTask.name)
        self.assertContains(response,self.uncategorizedTask.name)

    def test_category_filtering_month(self):
        url = reverse('filtered-month-view',args=[self.category1.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/calendar_month.html')
        self.assertContains(response,self.categorizedTask.name)
        self.assertNotContains(response,self.uncategorizedTask.name)

        url = reverse('month-view')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'calendar_app/calendar_month.html')
        self.assertContains(response,self.categorizedTask.name)
        self.assertContains(response,self.uncategorizedTask.name)
        