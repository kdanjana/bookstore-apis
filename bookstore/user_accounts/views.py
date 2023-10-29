from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import RegistrationSerializer
from user_accounts import models
# Create your views here.
# we are generating token when we are logging in user and registering a user, we are deleting token when user is logging out.

@api_view(['POST',])
def registration_view(request):
    """ generating a token when a user is registered"""
    if request.method == 'POST':
        serialiser = RegistrationSerializer(data=request.data)
        resp = {}
        if serialiser.is_valid():
            account_user = serialiser.save()
            resp['username'] = account_user.username
            resp['email'] = account_user.email
            token = Token.objects.get(user=account_user).key
            resp['token'] = token 
        else: 
            resp = serialiser.errors
            
        return Response(resp, status=status.HTTP_201_CREATED)
        
      
@api_view(['POST',])
def Logout_View(request):
    if request.method == 'POST':
        # deleted logged in user's token from the Token table
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        

