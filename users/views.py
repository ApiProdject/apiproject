from django.contrib.auth.models import User as UserRest
from users.models import User
from django.shortcuts import render

# Create your views here.
from users.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response

class UserCreationView(generics.CreateAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            UserRest.objects.create_user(username, 'email@email.com', password)
            user = User()
            user.login = username
            user.password = password
            user.user_level = 2
            user.save()
        return Response(status=status.HTTP_201_CREATED)