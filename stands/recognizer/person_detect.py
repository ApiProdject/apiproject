import os
import numpy as np
import cv2
import pickle
from apiproject.settings import STATIC_DIR


class Person():
    def __init__(self):
        self.embedder = cv2.dnn.readNetFromTorch(os.path.join(STATIC_DIR,
                                                     "models/openface_nn4.small2.v1.t7"))
        self.recognizer = pickle.loads(open(os.path.join(STATIC_DIR,
                                                     "models/recognizer.pickle"), "rb").read())
        self.le = pickle.loads(open(os.path.join(STATIC_DIR,
                                                     "models/le.pickle"), "rb").read())

    def person(self, face):
        faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                         (96, 96), (0, 0, 0), swapRB=True, crop=False)
        self.embedder.setInput(faceBlob)
        vec = self.embedder.forward()

        # perform classification to recognize the face
        preds = self.recognizer.predict_proba(vec)[0]
        j = np.argmax(preds)
        proba = preds[j]
        name = self.le.classes_[j]

        text = "{}: {:.2f}%".format(name, proba * 100)
        return text, name
