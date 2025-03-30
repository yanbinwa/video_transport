import os
import sys
import unittest
from pathlib import Path

from core.utils.video.video_srt_transfer import translate_srt_file

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

video_url = "https://www.youtube.com/watch?v=v0dgjSG4CpA"


class translate_srt_file_test(unittest.TestCase):

    def test_translate_srt_file(self):
        # 设置输入文件路径
        srt_file = os.path.join(project_root, "file", "v1.srt")
        translate_srt_file(srt_file)
