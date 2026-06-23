import cv2
import numpy as np


def detect_video_type(video_path):

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()

    cap.release()

    if not ret:
        return "LANE"

    frame = cv2.resize(
        frame,
        (1280, 720)
    )

    roi = frame[
        100:250,
        180:330
    ]

    hsv = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2HSV
    )

    # đỏ
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    red_mask = (
        cv2.inRange(
            hsv,
            lower_red1,
            upper_red1
        )
        +
        cv2.inRange(
            hsv,
            lower_red2,
            upper_red2
        )
    )

    # xanh
    lower_green = np.array([40,40,40])
    upper_green = np.array([90,255,255])

    green_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    if (
        cv2.countNonZero(red_mask)
        > 500
        or
        cv2.countNonZero(green_mask)
        > 500
    ):
        return "REDLIGHT"

    return "LANE"