import numpy as np
import os
from rest_framework import generics
from rest_framework.response import Response
import cv2

from stands.serializers import StandDetailSerializer, StandListSerializer, ImageSerializer
from stands.models import Stand
from .recognizer.emotion_detect import Emotion
from .recognizer.person_detect import Person
from .recognizer.face_detect import faces


class StandCreateView(generics.CreateAPIView):
    serializer_class = StandDetailSerializer


class StandListView(generics.ListAPIView):
    serializer_class = StandListSerializer
    queryset = Stand.objects.all()


class StandDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StandDetailSerializer
    queryset = Stand.objects.all()


class ImageRecognizeView(generics.CreateAPIView):
    serializer_class = ImageSerializer
    queryset = Stand.objects.all()

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            frame = cv2.imdecode(np.fromstring(serializer.validated_data['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            face_list = faces(frame)
            emotion = Emotion()
            person = Person()
            text = ""
            name = ""
            for i in range(0, face_list.shape[2]):
                confidence = face_list[0, 0, i, 2]
                if confidence > 0.5:
                    box = face_list[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]

                    if fW < 20 or fH < 20:
                        continue

                    #person_text, name = person.person(face=face)
                    emotion_text = emotion.emotion(face=face)
                    text = emotion_text
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                                  (0, 255, 0), 2)
                    cv2.rectangle(rgbImage, (startX, startY), (endX, startY - 44), (0, 255, 0), cv2.FILLED)
                    #cv2.putText(rgbImage, person_text, (startX, y - 16),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(rgbImage, emotion_text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                print(name+" "+text)
                #os.chdir(r'C:\Users\gavri\Desktop\фото')
                #cv2.imwrite("image.jpg", rgbImage)
            return Response(serializer.data)


