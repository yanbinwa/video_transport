import unittest

from core.utils.srt import srt_download

url = "https://www.bilibili.com/video/BV19D6DYGEba/?spm_id_from=333.1007.tianma.2-2-4.click"


class SrtDownloadTest(unittest.TestCase):

    def test_get_bilibili_subtitle(self):
        subtitles = srt_download.get_bilibili_subtitle(url)
        print(subtitles)
        AssertionError(subtitles is not None)

