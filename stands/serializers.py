from rest_framework import serializers
from stands.models import Stand


class StandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = ('person', 'emotion', 'age', 'sex', 'people')


class StandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = '__all__'
