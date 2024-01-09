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
        self.assertEqual(response_duplicate.data, {'email': ['user with this email already exists.']})
        self.assertEqual(CustomUser.objects.count(), 1)


    def test_user_registration_failure_email(self):
        data = {
            'email': '',
            'password': 'blank',
            'password_confirm': 'blank'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['This field may not be blank.']})

    
    def test_user_registration_failure_password_small(self):
        data = {
            'email': 'testusershortpassword@example.com',
            'password': 'short',
            'password_confirm': 'short'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ["This password is too short. It must contain at least 8 characters."]})
        

    def test_user_registration_failure_password_different(self):
        data = {
            'email': 'testuserdifferentpassword@example.com',
            'password': 'invalidpassword',
            'password_confirm': 'different'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'non_field_errors': ['Passwords do not match.']})


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


class UserLogoutViewTest(APITestCase):
    def setUp(self):
        self.url_login = reverse('login')
        self.url = reverse('logout')
        self.user_data = {
            # 'email': 'testlogoutuser@test.com',
            'username': 'testlogoutuser@test.com',
            'password': 'testlogoutpassword'
        }
        self.user = CustomUser.objects.create(**self.user_data)
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])


    def test_user_logout_authenticated(self):
        self.assertTrue(self.user.is_authenticated)

        response = self.client.get(self.url)
        self.client.logout()

        self.assertFalse(self.user.is_authenticated)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Logout successfully.'})


# class UserProfileViewTest(APITestCase):
