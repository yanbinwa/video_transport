import unittest

from core.utils.video import video_split

video_path = "../../file/test.mp4"
output_dir = "../../file/spilt"


class VideoSpiltTest(unittest.TestCase):

    def test_detect_scene_and_spilt(self):
        video_split.detect_scene_and_spilt(video_path, output_dir)

