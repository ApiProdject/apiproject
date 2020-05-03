from rest_framework import serializers
from infoPoints.models import InfoPoint

class InfoPointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoPoint
        fields = ['id', 'standId', 'emotionTypeID', 'age', 'sex']