import unittest

from core.utils.video import video_extract_audio

video_path = "../../file/test.mp4"
output_dir = "../../file/extract/test.mp3"


class VideoSpiltTest(unittest.TestCase):

    def test_extract_audio(self):
        video_extract_audio.extract_audio(video_path, output_dir)

