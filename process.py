import re
import cv2
import numpy as np


def process(result, c, server):
    name = c.execute(f'SELECT * FROM people WHERE id = {result}').fetchall()[0][1]
    # 处理重名问题: 人名 + 数字
    idx = re.match(r'\d+', name)
    if idx:
        name = name[:-len(idx.group()[0])]
    server.send_message(name + '0')


def preprocess(img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    face_cascade = cv2.CascadeClassifier('model/cascade.xml')
    eye_cascade = cv2.CascadeClassifier('model/eye.xml')

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转为灰度图

    # 检测脸部
    faces = face_cascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        imgface = img[y:(y + h * 2 // 3), x:x + w]  # 脸的上三分之二才可能存在眼睛
        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        eyes = eye_cascade.detectMultiScale(imgface)
        eyecenter = []
        for (ex, ey, ew, eh) in eyes:
            eyecenter.append((x + ex + ew // 2, y + ey + eh // 2))
        if len(eyecenter) == 2:  # 正好有两个眼睛，开始处理旋转图像
            if eyecenter[0][0] > eyecenter[1][0]:
                t = eyecenter[0]
                eyecenter[0] = eyecenter[1]
                eyecenter[1] = t

            # cv2.rectangle(img,eyecenter[0],eyecenter[0],(0,0,0),10)
            # cv2.rectangle(img,eyecenter[1],eyecenter[1],(255,255,255),10)

            a = np.array([1, 0])  # 通过向量化来寻找图像需要旋转的角度
            b = np.array([eyecenter[1][0] - eyecenter[0][0], eyecenter[1][1] - eyecenter[0][1]])
            cos_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            angle = np.arccos(cos_angle) * 180 / np.pi
            if angle >= 40:
                break
            if eyecenter[1][1] < eyecenter[0][1]: angle = -angle

            rotatecenter = (
                int((eyecenter[1][0] + eyecenter[0][0]) // 2), int((eyecenter[1][1] + eyecenter[0][1]) // 2))
            height, width = img.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D(rotatecenter, angle, 1)
            img = cv2.warpAffine(img, rotation_matrix, (width, height))
        break
    faces = face_cascade.detectMultiScale(
        img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200),
        flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in faces:
        imgx = img[y:(y + h), x:(x + w)]
        imgx = cv2.resize(imgx, (300, 300))
        return imgx
    imgx = cv2.resize(img, (300, 300))
    return imgx


def detect(img):
    face_cascade = cv2.CascadeClassifier('model/cascade.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    return len(faces)
