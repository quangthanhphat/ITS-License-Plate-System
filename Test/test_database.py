import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from Database.vehicle_repository import get_vehicle_by_plate

plate = "51H12345"

vehicle = get_vehicle_by_plate(plate)

print("=== KET QUA TRA CUU ===")

if vehicle:
    print("Tim thay xe")
    print("ID:", vehicle["id"])
    print("Bien so:", vehicle["license_plate"])
    print("Chu xe:", vehicle["owner_name"])
    print("Loai xe:", vehicle["vehicle_type"])
else:
    print("Khong tim thay xe")