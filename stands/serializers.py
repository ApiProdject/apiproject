from rest_framework import serializers
from stands.models import Stand
from events.models import Event
from events.serializers import EventListSerializer


class StandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = ('person', 'emotion', 'age', 'sex', 'people', 'description', 'id', 'eventId')


class StandOwnerListSerializer(serializers.ModelSerializer):
    eventId = EventListSerializer()

    class Meta:
        model = Stand
        fields = '__all__'


class StandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = '__all__'


class ImageSerializer(serializers.Serializer):
    image = serializers.CharField()
    stand = serializers.PrimaryKeyRelatedField(queryset=Stand.objects.all())
