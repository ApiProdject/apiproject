from rest_framework import serializers
from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name',)


class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
