import os

import cv2
import numpy as np
import seaborn as sns
from deepface import DeepFace

video = "processed-79D495F4-F8A7-44C6-A566-D2C22EAF3F77-420A3FE7-4850-48BD-81EE-DF8B7A24436E.mp4"

cap = cv2.VideoCapture(video)
faces = []
while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_faces = DeepFace.extract_faces(
        img_path=frame,
        enforce_detection=False,
    )

    # filter confidence > 0 and facial_area['x'] != 0 and
    current_faces = list(
        map(
            lambda x: {**x, "face": frame},
            filter(
                lambda face: face["confidence"] > 0 and face["facial_area"]["x"] != 0 and face["facial_area"]["y"] != 0,
                current_faces,
            ),
        )
    )
    faces.extend(current_faces)

# sort faces based on confidence
faces = sorted(faces, key=lambda x: x["confidence"], reverse=True)
indices = np.round(np.linspace(0, len(faces) - 1, 20)).astype(int)

# get faces at indices
faces = [faces[i] for i in indices]

# create a dir name 'images/Lê Công Minh Khôi'
dir_name = "images/Lê Công Minh Khôi"
os.makedirs(dir_name, exist_ok=True)

# save faces['face'] to dir_name
for index, face in enumerate(faces):
    cv2.imwrite(f"{dir_name}/{index}.png", face["face"])