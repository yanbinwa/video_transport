import os
import unittest
from pathlib import Path

from core.utils.srt import srt_download

url = "https://www.youtube.com/watch?v=BN2rTaFUlxs"

project_root = Path(__file__).parent.parent

class SrtDownloadTest(unittest.TestCase):

    def test_get_bilibili_subtitle(self):
        subtitles = srt_download.get_subtitle(url)
        print(subtitles)
        AssertionError(subtitles is not None)


    def test_get_youbute_srt(self):
        srt_path = os.path.join(project_root, "file", "v1.srt")
        srt_download.get_srt_file(url, srt_path)
