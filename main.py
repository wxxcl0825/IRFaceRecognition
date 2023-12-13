import os
import sqlite3
from predict import predict
from train import train
from server import Server
import cv2

path = "../../Dataset/IRpic"


def initialize():
    try:
        model = cv2.face.LBPHFaceRecognizer()
        model.read('model/model.cv2')
    except:
        model = train(os.path.join(path, 'raw'))
        model.write('model/model.cv2')

    conn = sqlite3.connect(os.path.join(path, 'raw', 'names.db'))
    c = conn.cursor()
    return model, c


def main():
    model, c = initialize()
    s = Server(port=6124)
    while True:
        predict(os.path.join(path, 'work'), model, c, s)


if __name__ == "__main__":
    main()
