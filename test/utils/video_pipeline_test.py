import os
import sys
import unittest
from pathlib import Path

from core.utils.video.video_pipeline import process_youtube_video

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

video_url = "https://www.youtube.com/watch?v=GMSC95hEj2w"


class VideoPipelineTest(unittest.TestCase):

    def test_video_pipeline(self):
        # 设置输入文件路径
        base_path = os.path.join(project_root, "pipeline")
        process_youtube_video(video_url, base_path)
