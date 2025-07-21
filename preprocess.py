import cv2
import os

def collect_faces(name, save_dir="data/raw_faces"):
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")
    count = 0

    user_dir = os.path.join(save_dir, name)
    os.makedirs(user_dir, exist_ok=True)

    print("Collecting face data. Press 'q' to stop.")
    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            cv2.imwrite(f"{user_dir}/{count}.jpg", face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Collector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
            break

    cam.release()
    cv2.destroyAllWindows()
