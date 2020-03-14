from rest_framework import generics
from stands.serializers import StandDetailSerializer, StandListSerializer
from stands.models import Stand
# Create your views here.


class StandCreateView(generics.CreateAPIView):
    serializer_class = StandDetailSerializer


class StandListView(generics.ListAPIView):
    serializer_class = StandListSerializer
    queryset = Stand.objects.all()


class StandDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StandDetailSerializer
    queryset = Stand.objects.all()
