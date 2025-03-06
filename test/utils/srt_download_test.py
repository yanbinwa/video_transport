import unittest

from core.utils.srt import srt_download

url = "https://www.youtube.com/watch?v=y6E1L6KVwYw"


class SrtDownloadTest(unittest.TestCase):

    def test_get_bilibili_subtitle(self):
        subtitles = srt_download.get_subtitle(url)
        print(subtitles)
        AssertionError(subtitles is not None)

