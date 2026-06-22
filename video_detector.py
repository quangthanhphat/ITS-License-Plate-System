import cv2
import numpy as np
import os
import datetime

from ultralytics import YOLO

from Models.ocr_reader import OCRReader

from Database.vehicle_repository import (
    get_vehicle_by_plate
)

from Database.violation_repository import (
    add_violation
)

# ==========================
# Khởi tạo
# ==========================

os.makedirs("Output", exist_ok=True)

cap = cv2.VideoCapture("Input/demo.mp4")

model = YOLO("Models/best.pt")
ocr = OCRReader()

frame_count = 0

# tránh lưu trùng vi phạm
recorded_violations = set()

# ==========================
# Polygon làn xe máy
# ==========================

motor_lane = [
    (680, 80),
    (752, 80),
    (1280, 500),
    (1280, 720),
    (950, 720)
]

x_top = 680
y_top = 80

x_bottom = 950
y_bottom = 720

# ==========================
# Xử lý video
# ==========================

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    frame = cv2.resize(
        frame,
        (1280, 720)
    )

    # ==========================
    # Vẽ vùng làn xe máy
    # ==========================

    cv2.polylines(
        frame,
        [np.array(motor_lane, np.int32)],
        True,
        (0, 0, 255),
        3
    )

    cv2.line(
        frame,
        (x_top, y_top),
        (x_bottom, y_bottom),
        (255, 255, 0),
        2
    )

    # ==========================
    # YOLO
    # ==========================

    results = model(frame)

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            # ==========================
            # Cắt biển số
            # ==========================

            plate_crop = frame[
                y1:y2,
                x1:x2
            ]

            if plate_crop.size == 0:
                continue

            temp_path = "Output/temp.jpg"

            cv2.imwrite(
                temp_path,
                plate_crop
            )

            # ==========================
            # OCR
            # ==========================

            plate_text = ocr.read_text(
                temp_path
            )

            if plate_text == "":
                continue

            # ==========================
            # Database
            # ==========================

            vehicle = get_vehicle_by_plate(
                plate_text
            )

            if vehicle:
                vehicle_type = vehicle[
                    "vehicle_type"
                ]
            else:
                vehicle_type = (
                    "Khong tim thay"
                )

            # ==========================
            # Xác định làn
            # ==========================

            plate_y = (
                y1 + y2
            ) // 2

            boundary_x = int(
                x_top
                +
                (
                    (plate_y - y_top)
                    *
                    (x_bottom - x_top)
                    /
                    (y_bottom - y_top)
                )
            )

            if x2 >= boundary_x:

                lane_status = (
                    "LAN XE MAY"
                )

                status_color = (
                    0,
                    0,
                    255
                )

            else:

                lane_status = (
                    "LAN O TO"
                )

                status_color = (
                    0,
                    255,
                    0
                )

            # ==========================
            # Phát hiện vi phạm
            # ==========================

            violation_text = ""

            if (
                vehicle_type == "O to"
                and lane_status == "LAN XE MAY"
            ):
                violation_text = (
                    "VI PHAM LAN XE MAY"
                )

            elif (
                vehicle_type == "Xe may"
                and lane_status == "LAN O TO"
            ):
                violation_text = (
                    "VI PHAM LAN O TO"
                )

            # ==========================
            # Lưu database + ảnh bằng chứng
            # ==========================

            if (
                violation_text != ""
                and vehicle
            ):

                violation_key = (
                    plate_text,
                    violation_text
                )

                if (
                    violation_key
                    not in
                    recorded_violations
                ):

                    recorded_violations.add(
                        violation_key
                    )

                    timestamp = (
                        datetime.datetime.now()
                        .strftime("%Y%m%d_%H%M%S")
                    )

                    evidence_path = (
                        f"Output/{plate_text}_{timestamp}.jpg"
                    )

                    evidence_frame = frame.copy()

                    cv2.rectangle(
                        evidence_frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        evidence_frame,
                        violation_text,
                        (x1, y1 - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    cv2.putText(
                        evidence_frame,
                        f"Plate: {plate_text}",
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

                    cv2.imwrite(
                        evidence_path,
                        evidence_frame
                    )

                    success = add_violation(
                        vehicle["id"],
                        violation_text,
                        evidence_path
                    )

                    if success:

                        print(
                            f"[VI PHAM] "
                            f"{plate_text} - "
                            f"{violation_text}"
                        )

            # ==========================
            # Hiển thị
            # ==========================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                status_color,
                2
            )

            cv2.putText(
                frame,
                plate_text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                status_color,
                2
            )

            cv2.putText(
                frame,
                vehicle_type,
                (x1, y2 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                lane_status,
                (x1, y2 + 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                status_color,
                2
            )

            if violation_text != "":

                cv2.putText(
                    frame,
                    violation_text,
                    (x1, y2 + 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2
                )

    cv2.putText(
        frame,
        f"Frame: {frame_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Traffic Video",
        frame
    )

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# ==========================
# Kết thúc
# ==========================

cap.release()
cv2.destroyAllWindows()

print("Hoan thanh xu ly video")