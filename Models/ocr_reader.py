import easyocr
import cv2


class OCRReader:

    def __init__(self):
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    def read_text(self, image_path):

        # Đọc ảnh
        image = cv2.imread(image_path)

        if image is None:
            return ""

        # Chuyển sang grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # OCR trên ảnh xám
        results = self.reader.readtext(
            gray
        )

        plate_text = ""

        for result in results:
            plate_text += result[1]

        plate_text = plate_text.upper()

        allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        plate_text = "".join(
            c for c in plate_text
            if c in allowed
        )

        return plate_text