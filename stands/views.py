from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from stands.serializers import StandDetailSerializer

from users.models import User
from stands.models import Stand
from stands.serializers import StandListSerializer

from user_stands.models import UserStand
from user_stands.serializers import UserStandListSerializer
from users.serializers import UserListSerializer
# Create your views here.


class StandCreateView(generics.CreateAPIView):
    serializer_class = StandDetailSerializer


class StandListView(generics.ListAPIView):
    serializer_class = StandListSerializer
    queryset = Stand.objects.all()

class StandByEventView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = StandListSerializer

    def get(self, request):
        eventId = self.request.query_params.get('eventid', None)
        isPrivate = self.request.query_params.get('isprivate', None)
        stands = []
        if isPrivate == '1':
            stands = []
            userName = request.user
            userId = UserListSerializer(User.objects.filter(login=userName), many=True).data[0]['id']
            userStands = UserStandListSerializer(UserStand.objects.filter(owner=userId), many=True).data
            for userStand in userStands:
                stands.append(StandListSerializer(Stand.objects.filter(id=userStand['id']), many=True).data[0])

        else:
            stands = Stand.objects.filter(eventId=eventId)
            stands = StandListSerializer(stands, many=True).data

        return Response(stands, status=status.HTTP_200_OK)


class StandDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StandDetailSerializer
    queryset = Stand.objects.all()
