import cv2
import numpy as np

from ultralytics import YOLO

from Models.ocr_reader import OCRReader

from Database.vehicle_repository import (
    get_vehicle_by_plate
)

from Database.violation_repository import (
    add_violation
)
import time
# ==========================
# VIDEO
# ==========================

cap = cv2.VideoCapture(
    "Input/redlight_demo.mp4"
)

# ==========================
# YOLO + OCR
# ==========================

model = YOLO("Models/best.pt")
ocr = OCRReader()

# ==========================
# CHỐNG LƯU TRÙNG
# ==========================

saved_violations = set()

# ==========================
# VẠCH DỪNG
# ==========================

STOP_LINE_Y = 390

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(
        frame,
        (1280, 720)
    )

    # ==========================
    # NHẬN DIỆN ĐÈN ĐỎ
    # ==========================

    roi = frame[
        100:250,
        180:330
    ]

    hsv = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2HSV
    )

    lower_red1 = np.array(
        [0, 120, 70]
    )

    upper_red1 = np.array(
        [10, 255, 255]
    )

    lower_red2 = np.array(
        [170, 120, 70]
    )

    upper_red2 = np.array(
        [180, 255, 255]
    )

    mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    mask = mask1 + mask2

    red_pixels = cv2.countNonZero(mask)

    if red_pixels > 1000:

        light_status = "RED"
        light_color = (0, 0, 255)

    else:

        light_status = "NOT RED"
        light_color = (0, 255, 0)

    # ==========================
    # HIỆN ĐÈN
    # ==========================

    cv2.rectangle(
        frame,
        (180, 100),
        (330, 250),
        light_color,
        2
    )

    cv2.putText(
        frame,
        f"LIGHT: {light_status}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        light_color,
        2
    )

    # ==========================
    # VẠCH DỪNG
    # ==========================

    cv2.line(
        frame,
        (0, STOP_LINE_Y),
        (1280, STOP_LINE_Y),
        (0, 255, 255),
        3
    )

    # ==========================
    # YOLO BIỂN SỐ
    # ==========================

    results = model(frame)

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # ------------------
            # Cắt biển số
            # ------------------

            plate_crop = frame[
                y1:y2,
                x1:x2
            ]

            cv2.imwrite(
                "Output/temp_plate.jpg",
                plate_crop
            )

            # ------------------
            # OCR
            # ------------------

            plate_text = ocr.read_text(
                "Output/temp_plate.jpg"
            )

            # ------------------
            # Tra DB
            # ------------------

            vehicle = get_vehicle_by_plate(
                plate_text
            )

            # ------------------
            # Khung biển số
            # ------------------

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # ------------------
            # Hiện biển số
            # ------------------

            cv2.putText(
                frame,
                plate_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            # ------------------
            # Loại xe
            # ------------------

            if vehicle:

                cv2.putText(
                    frame,
                    vehicle["vehicle_type"],
                    (x1, y1 - 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

            # ------------------
            # Tâm biển số
            # ------------------

            plate_center_y = (
                y1 + y2
            ) // 2

            cv2.circle(
                frame,
                (
                    (x1 + x2) // 2,
                    plate_center_y
                ),
                5,
                (255, 0, 0),
                -1
            )

            # ------------------
            # Kiểm tra vượt vạch
            # ------------------

            is_crossed = (
                plate_center_y >
                STOP_LINE_Y
            )

            # ------------------
            # Vượt đèn đỏ
            # ------------------

            if (
                light_status == "RED"
                and is_crossed
            ):

                cv2.putText(
                    frame,
                    "VUOT DEN DO",
                    (x1, y2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )







                if vehicle:
                    plate_key = vehicle[
                        "license_plate"]
                    if (
                        plate_key
                        not in saved_violations):
                        timestamp = int(
                            time.time()
                        )
                        violation_image = (
                            f"Output/redlight_{timestamp}.jpg")
                        cv2.imwrite(
                            violation_image,
                            frame)
                        add_violation(
                            vehicle["id"],
                            "Vuot Den Do",
                            violation_image)
                        saved_violations.add(
                            plate_key)
                        print(
                            f"Da luu vi pham: {plate_key}")



    cv2.imshow(
        "Red Light Detection",
        frame
    )

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()