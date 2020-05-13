import os

import cv2
import numpy as np

from apiproject.settings import STATIC_DIR
from stands.recognizer.SSRNET_model import SSR_net


class AgeRecognizer:
    __instance__ = None

    @staticmethod
    def get_instance():
        if not AgeRecognizer.__instance__:
            AgeRecognizer()
        return AgeRecognizer.__instance__

    def __init__(self):
        if AgeRecognizer.__instance__ is None:
            self.age_net = SSR_net(64, [3, 3, 3], 1, 1)()
            self.age_net.load_weights(os.path.join(STATIC_DIR, 'models/ssrnet_age_3_3_3_64_1.0_1.0.h5'))
            AgeRecognizer.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    def age(self, face):
        blob = cv2.resize(face, (64, 64))
        blob = cv2.normalize(blob, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        age = self.age_net.predict(np.expand_dims(blob, axis=0))
        return int(age)
