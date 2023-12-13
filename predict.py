import os
import cv2
from process import process, preprocess, detect


def predict(fp, model, c, server):
    if not os.listdir(fp):
        return
    file = os.path.join(fp, os.listdir(fp)[0])
    image = cv2.imread(file)
    if image is None:
        return
    if not detect(image):
        return
    image = preprocess(image)
    label, confidence = model.predict(image)
    if confidence > 50:
        label = 0
    while True:
        try:
            os.remove(file)
            break
        except:
            pass
    process(label, c, server)
