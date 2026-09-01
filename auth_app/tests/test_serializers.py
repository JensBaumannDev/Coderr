from django.test import TestCase
from auth_app.api.serializers import RegistrationSerializer, LoginSerializer
from auth_app.models import User

class RegistrationSerializerTest(TestCase):
    def test_valid_data(self):
        data = {
            "username": "testuser",
            "email": "test@coderr.com",
            "password": "123456789",
            "repeated_password": "123456789",
            "type": "customer",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@coderr.com",
            "password": "01234",
            "repeated_password": "012345",
            "type": "customer",
        }
        serializer = RegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
class LoginSerializerTest(TestCase):
    def test_valid_credentials(self):
        User.objects.create_user(username="testuser", password="123456", type="customer")
        data = {
            "username": "testuser",
            "password": "123456",
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_credentials(self):
        User.objects.create_user(username="testuser", password="1234", type="customer")
        data = {
            "username": "123",
            "password": "1234",
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())