import numpy as np
import pandas as pd
from deepface import DeepFace


def recognize(frame: np.ndarray) -> list[pd.DataFrame]:
    recognized_faces = DeepFace.find(
        img_path=frame,
        db_path="images",
        model_name="Facenet512",
        enforce_detection=False,
        detector_backend="opencv",
        silent=True,
    )

    results = []
    for recognized_face in recognized_faces:
        # filter source_x and source_y != 0
        recognized_face = recognized_face[recognized_face["source_x"] != 0]
        recognized_face = recognized_face[recognized_face["source_y"] != 0]

        # No face in frame
        if recognized_face.empty:
            continue

        # Get name of person
        recognized_face["name"] = recognized_face["identity"].str.split("/").str[1]

        # Append to results
        results.append(recognized_face)

    return results
