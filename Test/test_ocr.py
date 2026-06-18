from Models.ocr_reader import OCRReader


def test_ocr():

    image_path = "Output/plate_1.jpg"

    ocr = OCRReader()

    result = ocr.read_text(image_path)

    print("Kết quả OCR:")
    print(result)


if __name__ == "__main__":
    test_ocr()