import unittest

from core.utils.video import video_download

url = "https://www.youtube.com/watch?v=QNl3wbjXLT8"
out_file = "audio.mp3"


class VideoDownloadTest(unittest.TestCase):

    def test_download_audio_by_url(self):
        video_download.download_audio_by_url(url, "test.mp3")

