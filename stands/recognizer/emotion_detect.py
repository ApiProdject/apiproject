import os
import cv2
import numpy as np
from keras.models import load_model
from apiproject.settings import STATIC_DIR


class EmotionRecognizer:
    __instance__ = None

    @staticmethod
    def get_instance():
        if not EmotionRecognizer.__instance__:
            EmotionRecognizer()
        return EmotionRecognizer.__instance__

    def __init__(self):
        if EmotionRecognizer.__instance__ is None:
            self.emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
            self.model = load_model(os.path.join(STATIC_DIR, "models/model.h5"))
            EmotionRecognizer.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    def emotion(self, face):
        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(gray, (48, 48)), -1), 0)
        cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
        prediction = self.model.predict(cropped_img)
        return int(np.argmax(prediction)), "{:.2f}%".format(np.max(prediction) * 100)
