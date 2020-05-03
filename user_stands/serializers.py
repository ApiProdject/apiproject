from rest_framework import serializers
from user_stands.models import UserStand

class UserStandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStand
        fields = ('id', 'owner', 'standId')