from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user_stands.serializers import UserStandListSerializer
from users.models import User

from user_stands.models import UserStand
from users.serializers import UserListSerializer

from matches.models import Match
from matches.serializers import MatchListSerializer


class MatchByStandView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        standId = self.request.query_params.get('standid', None)
        isOwner = None
        matches = []

        userName = request.user
        userId = UserListSerializer(User.objects.filter(login=userName), many=True).data[0]['id']
        userStands = UserStandListSerializer(UserStand.objects.filter(owner=userId), many=True).data
        for userStand in userStands:
            if(str(userStand['standId']) == standId):
                isOwner = True

        if isOwner != None:
            matches = Match.objects.filter(standID=standId)
            matches = MatchListSerializer(matches, many=True).data

        return Response(matches, status=status.HTTP_200_OK)