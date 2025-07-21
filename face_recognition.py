import os
import cv2
import numpy as np

def train_recognizer(data_path="data/raw_faces", model_save_path="models/face_recognizer.pkl"):
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for person_name in os.listdir(data_path):
        person_dir = os.path.join(data_path, person_name)
        if not os.path.isdir(person_dir):
            continue

        label_map[current_label] = person_name
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(current_label)
        current_label += 1

    recognizer.train(faces, np.array(labels))
    recognizer.save(model_save_path)

    # Save label mapping
    with open("models/labels.txt", "w") as f:
        for label, name in label_map.items():
            f.write(f"{label}:{name}\n")
