from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def test_create_user_with_type(self):
        user = get_user_model().objects.create_user(username="testuser", password="testpass123", type="business")
        self.assertEqual(user.type, "business")
    
    def test_string_representation(self):
        user = get_user_model().objects.create_user(username="testuser", password="testpass123", type="business")
        self.assertEqual(str(user), "testuser")