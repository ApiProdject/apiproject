from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
import numpy as np
import os
from rest_framework import generics, status
from rest_framework.response import Response
import cv2

from stands.serializers import StandDetailSerializer, StandListSerializer, ImageSerializer
from stands.models import Stand
from stands.serializers import StandListSerializer

from user_stands.models import UserStand
from user_stands.serializers import UserStandListSerializer
from users.serializers import UserListSerializer
# Create your views here.
from emotionTypes.models import EmotionTypes
from matches.models import Match
from infoPoints.models import InfoPoint
from persons.models import Person
from .recognizer.emotion_detect import EmotionRecognizer
from .recognizer.person_detect import PersonRecognizer
from .recognizer.face_detect import FaceRecognizer


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


class ImageRecognizeView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Stand.objects.all()

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            stand = Stand.objects.get(id=serializer.data['stand'])
            frame = cv2.imdecode(np.fromstring(serializer.validated_data['image'].read(), np.uint8),
                                 cv2.IMREAD_UNCHANGED)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            face_recognizer = FaceRecognizer.get_instance()
            face_list = face_recognizer.faces(frame)

            for i in range(0, face_list.shape[2]):
                confidence = face_list[0, 0, i, 2]
                if confidence > 0.5:
                    box = face_list[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    if fW < 20 or fH < 20:
                        continue

                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    if stand.person:
                        match = Match()
                        match.standID = stand

                        person_recognizer = PersonRecognizer.get_instance()
                        person_text, text = person_recognizer.person(face=face)

                        name = text.split()

                        if len(name) == 2:
                            person = Person.objects.get(name=name[0], surname=name[1])
                        else:
                            if len(name) == 1:
                                try:
                                    person = Person.objects.get(name=name[0], surname=None)
                                except Exception:
                                    person = None
                        if person:
                            match.personId = person
                            print(person_text)
                            cv2.rectangle(frame, (startX, startY), (endX, startY - 44), (0, 255, 0), cv2.FILLED)
                            cv2.putText(frame, person_text, (startX, y - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                                        2)

                            if stand.emotion:
                                emotion = EmotionRecognizer.get_instance()
                                emotion_id, emotion_percent = emotion.emotion(face=face)
                                emotion_type = EmotionTypes.objects.get(emotion_number=emotion_id)
                                cv2.putText(frame, emotion_type.name + " (" + emotion_percent + ")", (startX, y),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                            (0, 0, 0), 2)
                                match.emotionId = emotion_type
                                print(emotion_type.name + " (" + emotion_percent + ")")

                            match.save()
                            # os.chdir(r'C:\Users\gavri\Desktop\фото')
                            # cv2.imwrite("image.jpg", frame)
                    else:
                        info_point = InfoPoint()
                        info_point.standId = stand
                        cv2.rectangle(frame, (startX, startY), (endX, startY - 44), (0, 255, 0), cv2.FILLED)

                        if stand.emotion:
                            emotion = EmotionRecognizer.get_instance()
                            emotion_id, emotion_percent = emotion.emotion(face=face)
                            emotion_type = EmotionTypes.objects.get(emotion_number=emotion_id)
                            cv2.putText(frame, emotion_type.name+" ("+emotion_percent+")", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                       (0, 0, 0), 2)
                            info_point.emotionTypeID = emotion_type
                            print(emotion_type.name+" ("+emotion_percent+")")

                        if stand.age:
                            info_point.age = 69
                            print(info_point.age)
                            pass

                        if stand.sex:
                            info_point.sex = InfoPoint.SEXES(1)
                            print(info_point.sex)
                            pass

                        info_point.save()
                        # os.chdir(r'C:\Users\gavri\Desktop\фото')
                        # cv2.imwrite("image.jpg", frame)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
