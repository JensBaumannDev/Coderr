from rest_framework.test import APITestCase
from rest_framework import status


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