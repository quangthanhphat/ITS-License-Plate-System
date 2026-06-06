"""
License Plate Detection Module

Nhiệm vụ:
- Nhận ảnh/video
- Phát hiện biển số
- Trả về vị trí biển số
"""

from typing import Dict, List


class PlateDetector:

    def __init__(self):
        self.model = None

    def load_model(self):
        """
        Sau này load YOLOv8 ở đây
        """
        pass

    def detect_plate(self, image) -> List[Dict]:

        # TODO:
        # YOLO inference

        return [
            {
                "bbox": [100, 150, 300, 220],
                "confidence": 0.95
            }
        ]

    def crop_plate(self, image, bbox):
        """
        Cắt vùng biển số
        Gửi sang OCR
        """

        # TODO
        return image

    def process(self, image):

        plates = self.detect_plate(image)

        return {
            "status": "success",
            "total_plates": len(plates),
            "plates": plates
        }