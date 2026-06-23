import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from video_classifier import (
    detect_video_type
)

result = detect_video_type(
    "Input/redlight_demo.mp4"
)

print(result)