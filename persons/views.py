from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from persons.models import Person
from persons.serializers import PersonListSerializer
from rest_framework.response import Response


class PeopleView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        people = PersonListSerializer(Person.objects.all(), many=True).data
        return Response(people, status=status.HTTP_200_OK)