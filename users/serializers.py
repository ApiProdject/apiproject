from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login', 'password', 'user_level']