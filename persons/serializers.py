from rest_framework import serializers
from persons.models import Person

class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'surname']