from rest_framework import serializers
from matches.models import Match


class MatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'personId', 'standID', 'emotionId']