import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from users.serializers import UserRegistrationSerializer

class UserRegistrationViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    
    def test_user_registration_sucess(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password_confirm': 'testpassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(username='testuser@example.com')
        self.assertIsNotNone(user)

        expected_response = {
            'user': UserRegistrationSerializer(user).data,
            'message': 'User registered successfully'
        }
        self.assertEqual(json.loads(response.content), expected_response)

    def test_user_registration_failure(self):
        data = {
            'email': '',
            'password': 'invalid',
            'password_confirm': 'short'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)