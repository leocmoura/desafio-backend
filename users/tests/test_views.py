import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser
from users.serializers import UserRegistrationSerializer

class UserRegistrationViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.user_data = {
            'email': 'testuser@teste.com',
            'username': 'testuser@teste.com',
            'password': ' testpassword',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    
    def test_user_registration_sucess(self):
        data = {
            'email': 'registrationuser@teste.com',
            'password': 'testpassword',
            'password_confirm': 'testpassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(username='registrationuser@teste.com')
        self.assertIsNotNone(user)

        expected_response = {
            'user': UserRegistrationSerializer(user).data,
            'message': 'User registered successfully'
        }
        self.assertEqual(json.loads(response.content), expected_response)


    def test_user_unique_email(self):
        data = {
            'email': 'testuser@teste.com',
            'password': 'uniquepass',
            'password_confirm': 'uniquepass'
        }

        response_duplicate = self.client.post(self.url, data, format='json')
        self.assertEqual(response_duplicate.status_code, status.HTTP_400_BAD_REQUEST)

        expected_response = {
            'email': ['user with this email already exists.']
        }
        self.assertEqual(json.loads(response_duplicate.content), expected_response)
        self.assertEqual(CustomUser.objects.count(), 1)


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
            'email': 'testusershortpassword@example.com',
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
            'email': 'testuserdifferentpassword@example.com',
            'password': 'invalidpassword',
            'password_confirm': 'different'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        expected_response = {
                'non_field_errors': ["Passwords do not match."]
        }
        self.assertEqual(json.loads(response.content), expected_response)

class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user_data = {
            'email': 'testloginuser@teste.com',
            'username': 'testloginuser@teste.com',
            'password': 'testpassword'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.valid_credentials = {
            'username': 'testloginuser@teste.com',
            'password': 'testpassword'
        }
        self.invalid_credentials = {
            'username': 'testloginuser@teste.com',
            'password': 'wrongtestpassword'
        }
        self.empty_credentials = {
            'username': '',
            'password': ''
        }


    def test_user_login_success(self):
        response = self.client.post(self.url, self.valid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Login successfully.'})


    def test_user_login_invalid(self):
        response = self.client.post(self.url, self.invalid_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'Invalid credentials.'})


    def test_user_login_empty(self):
        response = self.client.post(self.url, self.empty_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'Invalid credentials.'})