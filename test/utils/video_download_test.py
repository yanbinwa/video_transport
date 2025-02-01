import unittest

from core.utils.video import video_download

url = "https://www.youtube.com/watch?v=uBW-kRznAwo"
out_file = "audio.mp3"


class VideoDownloadTest(unittest.TestCase):

    def test_download_audio_by_url(self):
        video_download.download_audio_by_url(url, "../../file/test2.mp3")

    def test_download_video_by_url(self):
        video_download.download_video_by_url(url, "../../file/test2.mp4")
