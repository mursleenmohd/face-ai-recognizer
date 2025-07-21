import cv2
from utils import face_recognition
import os

# Load recognizer and labels
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/face_recognizer.pkl")

label_map = {}
with open("models/labels.txt") as f:
    for line in f:
        label, name = line.strip().split(":")
        label_map[int(label)] = name

face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        label, confidence = recognizer.predict(face)
        name = label_map[label] if confidence < 60 else "Unknown"

        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
