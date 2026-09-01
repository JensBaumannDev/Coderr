from rest_framework.test import APITestCase
from rest_framework import status
from auth_app.models import User


class RegistrationViewTest(APITestCase):
    def test_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@coderr.com",
            "password": "1234",
            "repeated_password": "1234",
            "type": "customer",
        }
        response = self.client.post("/api/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_password_mismatch(self):
        data = {
            "username": "testuser2",
            "email": "test2@coderr.com",
            "password": "1234",
            "repeated_password": "5678",
            "type": "customer",
        }
        response = self.client.post("/api/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_username(self):
        User.objects.create_user(
            username="duplicate",
            email="dup@coderr.com",
            password="testpass123",
            type="customer",
        )
        data = {
            "username": "duplicate",
            "email": "dup2@coderr.com",
            "password": "testpass123",
            "repeated_password": "testpass123",
            "type": "customer",
        }
        response = self.client.post("/api/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_field(self):
        data = {
            "email": "missing@coderr.com",
            "password": "testpass123",
            "repeated_password": "testpass123",
            "type": "customer",
        }
        response = self.client.post("/api/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_invalid_type(self):
        data = {
            "username": "invalidtype",
            "email": "invalidtype@coderr.com",
            "password": "testpass123",
            "repeated_password": "testpass123",
            "type": "foo",
        }
        response = self.client.post("/api/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(APITestCase):
    def test_login_success(self):
        User.objects.create_user(username="testuser", password="1234", type="customer")
        data = {
            "username": "testuser",
            "password": "1234",
        }
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        User.objects.create_user(username="testuser", password="1234", type="customer")
        data = {
            "username": "testuser2",
            "password": "1234",
        }
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)