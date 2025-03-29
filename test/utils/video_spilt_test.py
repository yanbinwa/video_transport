import os
import sys
import unittest
from pathlib import Path

from core.utils.video import video_split

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

class VideoSpiltTest(unittest.TestCase):

    def test_detect_scene_and_spilt(self):
        video_path = os.path.join(project_root, "file/output", "v1_with_subtitle.mp4")
        output_dir = os.path.join(project_root, "file/spilt")
        video_split.detect_scene_and_spilt(video_path, output_dir)

