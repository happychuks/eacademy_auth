from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.user_detail_url = reverse('user_detail')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_signup_short_password(self):
        short_password_data = self.user_data.copy()
        short_password_data['password'] = 'short'
        short_password_data['password2'] = 'short'
        response = self.client.post(self.signup_url, short_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_signup_mismatched_passwords(self):
        mismatched_password_data = self.user_data.copy()
        mismatched_password_data['password2'] = 'differentpassword'
        response = self.client.post(self.signup_url, mismatched_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login(self):
        self.client.post(self.signup_url, self.user_data)
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_detail(self):
        self.client.post(self.signup_url, self.user_data)
        login_response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        })
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_user_detail_unauthenticated(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)