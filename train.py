import os
import cv2
import numpy as np
import sqlite3
import face_recognition as fr


def train(fp):  # -> cv2.face.LBPHFaceRecognizer:
    files = os.listdir(fp)

    images = []
    names = []

    for file in files:
        if '.db' in file:
            continue
        images.append(cv2.imread(os.path.join(fp, file)))
        names.append(file.split('.')[0])
    # labels = np.arange(len(images)) + 1
    # model = cv2.face.LBPHFaceRecognizer_create()
    # model.train(images, labels)
    model = [fr.face_encodings(image, fr.face_locations(image))[0] for image in images]

    if os.path.exists(os.path.join(fp, 'names.db')):
        os.remove(os.path.join(fp, 'names.db'))
    conn = sqlite3.connect(os.path.join(fp, 'names.db'))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')
    c.execute("INSERT INTO people (id, name) VALUES (0, '陌生人')")
    for name in names:
        c.execute(f"INSERT INTO people (name) VALUES ('{name}')")
    conn.commit()
    conn.close()
    return model
