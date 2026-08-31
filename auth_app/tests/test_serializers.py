from django.test import TestCase
from auth_app.api.serializers import RegistrationSerializer


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
