import base64

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
import numpy as np
import os
from rest_framework import generics, status
from rest_framework.response import Response
import cv2

from stands.serializers import StandDetailSerializer, StandListSerializer, ImageSerializer, StandOwnerListSerializer
from stands.models import Stand

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
from .recognizer.age_detect import AgeRecognizer
from .recognizer.gender_detect import GenderRecognizer



class StandCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = StandDetailSerializer

    def post(self, request):
        userName = request.user
        serializer = StandDetailSerializer(data=request.data)
        if serializer.is_valid():
            stand = serializer.save()
            user_stand = UserStand()
            user_stand.standId = stand
            user_stand.owner = User.objects.filter(login=userName)[0]
            user_stand.save()
            return Response(StandOwnerListSerializer(stand).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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


class StandByUserView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = StandListSerializer

    def get(self, request):
        stands = []
        userName = request.user
        userId = UserListSerializer(User.objects.filter(login=userName), many=True).data[0]['id']
        userStands = UserStandListSerializer(UserStand.objects.filter(owner=userId), many=True).data
        for userStand in userStands:
            stands.append(StandOwnerListSerializer(Stand.objects.filter(id=userStand['standId']), many=True).data[0])

        return Response(stands, status=status.HTTP_200_OK)


class StandDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StandDetailSerializer
    queryset = Stand.objects.all()


def to_base64(img):
    _, buf = cv2.imencode(".png", img)
    return base64.b64encode(buf)


def from_base64(buf):
    buf_decode = base64.b64decode(buf)
    buf_arr = np.fromstring(buf_decode, dtype=np.uint8)
    return cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)


class ImageRecognizeView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Stand.objects.all()

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            stand = Stand.objects.get(id=serializer.data['stand'])
            frame = from_base64(serializer.data['image'])
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
                    cv2.rectangle(frame, (startX, startY), (endX, startY - 66), (0, 255, 0), cv2.FILLED)
                    y = startY - 10 if startY - 10 > 10 else startY + 10

                    emotion_type = None
                    if stand.emotion:
                        emotion = EmotionRecognizer.get_instance()
                        emotion_id, emotion_percent = emotion.emotion(face=face)
                        emotion_type = EmotionTypes.objects.get(emotion_number=emotion_id)
                        cv2.putText(frame, emotion_type.name + " (" + emotion_percent + ")", (startX, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 0, 0), 2)
                        print(emotion_type.name + " (" + emotion_percent + ")")

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
                            cv2.putText(frame, person_text, (startX, y - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),
                                        2)

                            if stand.emotion:
                                match.emotionId = emotion_type

                            # match.save()
                            # os.chdir(r'C:\Users\gavri\Desktop\фото')
                            # cv2.imwrite("image.jpg", frame)
                    info_point = InfoPoint()
                    info_point.standId = stand

                    if stand.emotion:
                        info_point.emotionTypeID = emotion_type

                    text = ''
                    if stand.age:
                        age_recognizer = AgeRecognizer.get_instance()
                        age = age_recognizer.age(face=face)
                        info_point.age = age
                        text = str(info_point.age) + ', '
                        print(info_point.age)

                    if stand.sex:
                        sex_recognizer = GenderRecognizer.get_instance()
                        sex = sex_recognizer.gender(face=face)
                        info_point.sex = sex
                        text += str(info_point.SEXES[sex - 1][1])
                        print(info_point.SEXES[sex - 1][1])

                    cv2.putText(frame, text, (startX, y - 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    # info_point.save()
                    # os.chdir(r'C:\Users\gavri\Desktop\фото')
                    # cv2.imwrite("image.jpg", frame)


            return Response(to_base64(frame), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
