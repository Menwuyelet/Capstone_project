from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'non_field_errors': ['Unable to log in with provided credentials.']}, status=400)

        # Create or get the token
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})