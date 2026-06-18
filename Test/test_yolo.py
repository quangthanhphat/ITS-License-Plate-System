from Models.plate_detector import PlateDetector


def test_yolo():

    image_path = "Input/test.jpg"

    detector = PlateDetector()

    saved_plates = detector.save_detected_plates(
        image_path=image_path,
        output_folder="Output"
    )

    print(f"Tìm thấy {len(saved_plates)} biển số")

    for plate in saved_plates:
        print(f"Đã lưu: {plate}")


if __name__ == "__main__":
    test_yolo()
