import unittest

from core.utils.video import video_download

url = "https://www.youtube.com/shorts/hG4tGl0s7XU"
out_file = "audio.mp3"


class VideoDownloadTest(unittest.TestCase):

    def test_download_audio_by_url(self):
        video_download.download_audio_by_url(url, "test.mp3")

