import unittest

from core.utils.video import video_download

url = "https://www.youtube.com/watch?v=BN2rTaFUlxs"
video_file = "../../file/test2.mp4"
audio_file = "../../file/v1.mp3"

class VideoDownloadTest(unittest.TestCase):

    def test_download_audio_by_url(self):
        video_download.download_audio_by_url(url, audio_file)

    def test_download_video_by_url(self):
        video_download.download_video_by_url(url, video_file)
