from Models.video_processor import VideoProcessor


def test_video():

    processor = VideoProcessor()

    processor.process_video(
        "Input/test_video.mp4"
    )


if __name__ == "__main__":
    test_video()