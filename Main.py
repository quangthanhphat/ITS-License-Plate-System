from Models.plate_detector import PlateDetector
from Models.ocr_reader import OCRReader

from Database.vehicle_repository import (
    get_vehicle_by_plate
)

from Database.violation_repository import (
    add_violation
)


def main():

    image_path = "Input/test.jpg"

    detector = PlateDetector()
    ocr = OCRReader()

    print("Đang phát hiện biển số...")

    saved_plates = detector.save_detected_plates(
        image_path=image_path,
        output_folder="Output"
    )

    if len(saved_plates) == 0:
        print("Không phát hiện biển số.")
        return

    print(f"Đã phát hiện {len(saved_plates)} biển số.\n")

    for plate_path in saved_plates:

        plate_text = ocr.read_text(
            plate_path
        )

        print(f"Biển số nhận diện: {plate_text}")

        vehicle = get_vehicle_by_plate(
            plate_text
        )

        if vehicle:

            print("=== THÔNG TIN XE ===")
            print(f"Biển số: {vehicle['license_plate']}")
            print(f"Chủ xe: {vehicle['owner_name']}")
            print(f"Loại xe: {vehicle['vehicle_type']}")

            success = add_violation(
                vehicle['id'],
                "Vuot den do",
                plate_path
            )

            if success:
                print("Đã ghi vi phạm vào database")
            else:
                print("Ghi vi phạm thất bại")

        else:

            print("Không tìm thấy xe trong database")

        print()


if __name__ == "__main__":
    main()