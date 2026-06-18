from ultralytics import YOLO
import cv2
import os


class PlateDetector:

    def __init__(self, model_path="Models/best.pt"):
        self.model = YOLO(model_path)

    def detect_plate(self, image_path):

        results = self.model(image_path)

        image = cv2.imread(image_path)

        detected_plates = []

        for result in results:

            for box in result.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                plate_crop = image[y1:y2, x1:x2]

                detected_plates.append(
                    {
                        "bbox": (x1, y1, x2, y2),
                        "crop": plate_crop
                    }
                )

        return detected_plates

    def save_detected_plates(
        self,
        image_path,
        output_folder="Output"
    ):

        os.makedirs(output_folder, exist_ok=True)

        plates = self.detect_plate(image_path)

        saved_paths = []

        for index, plate in enumerate(plates):

            save_path = os.path.join(
                output_folder,
                f"plate_{index + 1}.jpg"
            )

            cv2.imwrite(
                save_path,
                plate["crop"]
            )

            saved_paths.append(save_path)

        return saved_paths