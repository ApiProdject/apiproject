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


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False, max_length=None, allow_empty_file=False, use_url=False)
    stand = serializers.PrimaryKeyRelatedField(queryset=Stand.objects.all())
