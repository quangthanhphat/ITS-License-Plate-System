import cv2
import os


class VideoProcessor:

    def __init__(self):
        self.capture_count = 0

    def process_video(
        self,
        video_path,
        output_folder="Output"
    ):

        os.makedirs(output_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Không thể mở video.")
            return

        print("Video đang chạy...")
        print("Nhấn S để chụp ảnh vi phạm")
        print("Nhấn Q để thoát")

        while True:

            ret, frame = cap.read()

            if not ret:
                print("Đã đọc hết video.")
                break

            cv2.imshow(
                "Traffic Monitoring",
                frame
            )

            key = cv2.waitKey(25) & 0xFF

            # Nhấn S để lưu ảnh
            if key == ord('s'):

                self.capture_count += 1

                image_path = os.path.join(
                    output_folder,
                    f"evidence_{self.capture_count:03d}.jpg"
                )

                cv2.imwrite(
                    image_path,
                    frame
                )

                print(
                    f"Đã lưu: {image_path}"
                )

            # Nhấn Q để thoát
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()