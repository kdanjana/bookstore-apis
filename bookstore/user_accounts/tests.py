from typing import Any
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import  APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Create your tests here.

class UserAccountsTestCase(TestCase):
    """ test user registration,login and logout """
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser2",password="test@12345")
        
        
    def test_user_registration(self):
        data = {
            "username": "testuser1",
            "email": "t@g.com",
            "password": "pwd12345",
            "password2": "pwd12345",
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_user_login(self):
        data1 = {
            "username": "testuser2",
            "password": "test@12345"
        }
        data2 = {
            "username": "testuser2",
            "password": "pwd12345"
        }
        response = self.client.post(reverse('login'), data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('login'), data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_logout(self):
        self.token = Token.objects.get(user__username="testuser2")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)