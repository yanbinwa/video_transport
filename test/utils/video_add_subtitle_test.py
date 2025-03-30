import os
import unittest
from pathlib import Path

from core.utils.video.video_add_subtitle import add_subtitle_to_video

project_root = Path(__file__).parent.parent.parent


class VideoAddSubtitleTest(unittest.TestCase):

    def test_video_add_subtitle(self):
        """
            测试向视频添加字幕功能
            """
        # 设置输入文件路径
        video_path = os.path.join(project_root, "file", "v1_mixed.mp4")
        srt_path = os.path.join(project_root, "file", "v1_zh-cn.srt")

        # 设置输出文件路径
        output_dir = os.path.join(project_root, "file", "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "v1_with_subtitle_v1.mp4")

        try:
            # 执行添加字幕
            result_path = add_subtitle_to_video(
                video_path=video_path,
                srt_path=srt_path,
                output_path=output_path,
                fontsize=40,  # 稍微大一点的字体
                color='white',
                stroke_color='white',
                stroke_width=2,  # 稍微粗一点的描边
                y_position=0.25  # 字幕位置设置为从底部向上25%的位置
            )
            print(f"✅ 字幕添加成功！输出文件：{result_path}")

            # 验证输出文件是否存在
            assert os.path.exists(result_path), "输出文件不存在"
            assert os.path.getsize(result_path) > 0, "输出文件大小为0"

            print("✅ 测试通过！")
            return True

        except Exception as e:
            print(f"❌ 测试失败：{str(e)}")
            return False
