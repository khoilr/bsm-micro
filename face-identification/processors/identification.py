from processors.recognize import recognize
from processors.detection import detect


def identify(frame):
    results = recognize(frame)

    for result in results:
        recognized_face = result.groupby("name").filter(lambda x: len(x) >= 3 and len(x) == len(x.max()))

        if recognized_face.empty:
            print("stranger")
        else:
            print("known person")
