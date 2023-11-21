import cv2
import pandas as pd


def calculate_extended_bbox(x, y, w, h, frame_shape, extend_by=20) -> tuple:
    extended_x = max(0, x - extend_by)
    extended_y = max(0, y - extend_by)
    extended_w = min(frame_shape[1] - extended_x, w + 2 * extend_by)
    extended_h = min(frame_shape[0] - extended_y, h + 2 * extend_by)

    return extended_x, extended_y, extended_w, extended_h


def draw_info(frame, face: dict):
    x = face["source_x"]
    y = face["source_y"]
    w = face["source_w"]
    h = face["source_h"]

    extended_bbox = calculate_extended_bbox(x, y, w, h, frame.shape, extend_by=20)
    color = (255, 255, 0)
    thickness = 2

    # draw rectangle wrap face
    image = cv2.rectangle(
        frame,
        (extended_bbox[0], extended_bbox[1]),
        (extended_bbox[0] + extended_bbox[2], extended_bbox[1] + extended_bbox[3]),
        color,
        thickness,
    )

    # write name on the rectangle
    image = cv2.putText(
        image,
        str(face["name"]),
        (extended_bbox[0] - 10, extended_bbox[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        thickness,
    )

    return image
