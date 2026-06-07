
logging.basicConfig(level=logging.INFO, format='%(asctime)s - OCR: %(message)s')
logger = logging.getLogger(__name__)


class MockLicensePlateOCR:
    def __init__(self):
        logger.info("Khởi tạo hệ thống Mock OCR...")
        self.is_ready = True

    def preprocess_image(self, image: Any) -> Any:
        logger.info("Xử lý ảnh...")
        time.sleep(0.5)
        return image

    def extract_text(self, image: Any) -> str:
        logger.info("Đang nhận diện ký tự...")
        time.sleep(1.0)
        return random.choice(["59A-123.45", "30F-999.99", "43C-112.33", "65B-888.88"])


def read_plate(image: Any) -> Dict[str, Any]:
    logger.info("Bắt đầu xử lý ảnh mới...")

    ocr_system = MockLicensePlateOCR()
    processed_img = ocr_system.preprocess_image(image)
    plate_text = ocr_system.extract_text(processed_img)
    confidence_score = round(random.uniform(0.92, 0.99), 2)

    logger.info(f"Hoàn tất: [{plate_text}] - {confidence_score}")

    return {
        "status": "success",
        "message": "Thành công",
        "license_plate": plate_text,
        "confidence": confidence_score
    }


if __name__ == "__main__":
    print(read_plate("test.jpg"))
