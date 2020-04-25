import os

import cv2
from apiproject.settings import STATIC_DIR


def faces(frame):
    detector = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR,
                                                     "models/deploy.prototxt"),
                                        os.path.join(STATIC_DIR,
                                                     "models/res10_300x300_ssd_iter_140000.caffemodel"))

    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    return detector.forward()
