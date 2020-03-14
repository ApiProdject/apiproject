from rest_framework import generics
from events.serializers import EventDetailSerializer, EventListSerializer
from events.models import Event
# Create your views here.


class EventCreateView(generics.CreateAPIView):
    serializer_class = EventDetailSerializer


class EventListView(generics.ListAPIView):
    serializer_class = EventListSerializer
    queryset = Event.objects.all()


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventDetailSerializer
    queryset = Event.objects.all()
