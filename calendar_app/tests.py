from django.test import TestCase
from .models import CustomUser
from django.db.utils import IntegrityError
# Create your tests here.

# Index view template
class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/index.html')

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
