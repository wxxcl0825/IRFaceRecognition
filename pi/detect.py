import cv2


def detect(fp: str) -> bool:
    face_cascade = cv2.CascadeClassifier('data.xml')
    img = cv2.imread(fp)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    return len(faces)
