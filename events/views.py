from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from events.serializers import EventDetailSerializer, EventListSerializer
from events.models import Event
from users.models import User
from stands.models import Stand
from stands.serializers import StandListSerializer

from user_stands.models import UserStand
from user_stands.serializers import UserStandListSerializer
from users.serializers import UserListSerializer


class EventCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = EventDetailSerializer


class EventListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = EventListSerializer

    def get(self, request):
        isPrivate = self.request.query_params.get('isprivate', None)
        events = []
        if isPrivate == '1':
            stands = []
            userName = request.user
            userId = UserListSerializer(User.objects.filter(login=userName), many=True).data[0]['id']
            userStands = UserStandListSerializer(UserStand.objects.filter(owner=userId), many=True).data
            for userStand in userStands:
                stands.append(StandListSerializer(Stand.objects.filter(id=userStand['id']), many=True).data[0])

            for stand in stands:
                events.append(EventListSerializer(Event.objects.filter(id=stand['eventId']), many=True).data[0])

            uniqueEvents = []
            for event in events:
                if event not in uniqueEvents:
                    uniqueEvents.append(event)

            events = uniqueEvents

        else:
            events = Event.objects.all()
            events = EventListSerializer(events, many=True).data

        return Response(events, status=status.HTTP_200_OK)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
