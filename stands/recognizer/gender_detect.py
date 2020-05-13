import os

import cv2
import numpy as np

from apiproject.settings import STATIC_DIR
from infoPoints.models import InfoPoint
from stands.recognizer.SSRNET_model import SSR_net_general


class GenderRecognizer:
    __instance__ = None

    @staticmethod
    def get_instance():
        if not GenderRecognizer.__instance__:
            GenderRecognizer()
        return GenderRecognizer.__instance__

    def __init__(self):
        if GenderRecognizer.__instance__ is None:
            self.gender_net = SSR_net_general(64, [3, 3, 3], 1, 1)()
            self.gender_net.load_weights(os.path.join(STATIC_DIR, 'models/ssrnet_gender_3_3_3_64_1.0_1.0.h5'))
            GenderRecognizer.__instance__ = self
        else:
            raise Exception("This class is a singleton!")

    def gender(self, face):
        blob = cv2.resize(face, (64, 64))
        blob = cv2.normalize(blob, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        gender = self.gender_net.predict(np.expand_dims(blob, axis=0))
        return 1 if (gender >= 0.5) else 2
