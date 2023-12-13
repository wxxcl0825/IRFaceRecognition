import os
import cv2
from process import process, preprocess, detect
import face_recognition as fr
import numpy as np


def predict(fp, model, c, server):
    if not os.listdir(fp):
        return
    file = os.path.join(fp, os.listdir(fp)[0])
    image = cv2.imread(file)
    if image is None:
        return
    if not detect(image):
        return
    # image = preprocess(image)
    # label, confidence = model.predict(image)
    encoding = fr.face_encodings(image, fr.face_locations(image))
    if not encoding:
        while True:
            try:
                os.remove(file)
                break
            except:
                pass
        return
    dis = fr.face_distance(model, encoding[0])
    print(dis)
    label = np.argmin(dis)
    confidence = dis[label]
    label += 1
    if confidence > 0.4:
        label = 0
    while True:
        try:
            os.remove(file)
            break
        except:
            pass
    process(label, c, server)
