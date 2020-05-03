from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from infoPoints.models import InfoPoint
from infoPoints.serializers import InfoPointListSerializer


class InfoPointListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        standId = self.request.query_params.get('standid', None)
        infoPoints = InfoPointListSerializer(InfoPoint.objects.filter(standId=standId), many=True).data
        return Response(infoPoints, status=status.HTTP_200_OK)