import os

import cv2
from apiproject.settings import STATIC_DIR


class FaceRecognizer:
    __instance__ = None

    @staticmethod
    def get_instance():
        if not FaceRecognizer.__instance__:
            FaceRecognizer()
        return FaceRecognizer.__instance__

    def __init__(self):
        if FaceRecognizer.__instance__ is None:
            self.detector = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR,
                                                     "models/deploy.prototxt"),
                                        os.path.join(STATIC_DIR,
                                                     "models/res10_300x300_ssd_iter_140000.caffemodel"))
            FaceRecognizer.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    def faces(self, frame):
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        self.detector.setInput(imageBlob)
        return self.detector.forward()
