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

    def test_user_registration_failure_email(self):
        data = {
            'email': '',
            'password': 'blank',
            'password_confirm': 'blank'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_response = {
            'email': ['This field may not be blank.']
        }
        self.assertEqual(json.loads(response.content), expected_response)

    
    def test_user_registration_failure_password_small(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'short',
            'password_confirm': 'short'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_response = {
                'non_field_errors': ["This password is too short. It must contain at least 8 characters."]
        }
        self.assertEqual(json.loads(response.content), expected_response)
        
    def test_user_registration_failure_password_different(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'invalidpassword',
            'password_confirm': 'different'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_response = {
                'non_field_errors': ["Passwords do not match."]
        }
        self.assertEqual(json.loads(response.content), expected_response)