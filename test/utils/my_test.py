# 添加项目根目录到 Python 路径
import os.path
import sys
from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip

from core.utils.common.logger import log

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    video_path = os.path.join(project_root, "file", "v1_mixed.mp4")
    # 2. 检查视频是否有音频，如果没有则下载并合并
    video = VideoFileClip(video_path)
    if video.audio is None:
        log.info("视频没有音频，开始下载音频")
        # 下载音频