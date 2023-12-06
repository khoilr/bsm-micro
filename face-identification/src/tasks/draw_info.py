import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


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

    extended_bbox = calculate_extended_bbox(x, y, w, h, frame.shape, extend_by=10)
    color = (0, 255, 0)
    thickness = 1

    # draw rectangle wrap face
    image = cv2.rectangle(
        frame,
        (extended_bbox[0], extended_bbox[1]),
        (extended_bbox[0] + extended_bbox[2], extended_bbox[1] + extended_bbox[3]),
        color,
        thickness,
    )

    # write name on the rectangle
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    font = ImageFont.truetype("src/fonts/JosefinSans-VariableFont_wght.ttf", 20)
    draw = ImageDraw.Draw(pil_image)
    draw.text(
        xy=(extended_bbox[0] - 10, extended_bbox[1] - 10),
        text=str(face["name"]),
        fill="green",
        font=font,
        stroke_fill="green",
        stroke_width=1,
        thickness=1,
    )
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    return image
