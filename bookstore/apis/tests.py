from typing import Any
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import  APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Author, Book, Review
from .serializers import AuthorModSerializer, BookModSerializer, ReviewModSerializer



class AuthorTestCase(TestCase):
    """ test the operations on Author model by normal user"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser",password="pwd@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_authorslist(self):
        """ tests if  normal logged in user can get list of authors"""
        resp = self.client.get(reverse('authors_list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_author_add(self):
        """ tests if  normal logged in user can add new author to list"""
        new_book = {
            "first_name": "test1",
            "last_name": "user1",
            "address": "local"
        }
        resp = self.client.post(reverse('authors_list'), new_book)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_author_delete(self):
        pass
    
    def test_author_details_update(self):
        pass