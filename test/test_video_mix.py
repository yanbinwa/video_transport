import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from core.utils.video.video_mix_audio import mix_video_audio

def test_mix_video_audio():
    """
    测试视频和音频混合功能
    """
    # 设置输入文件路径
    video_path = os.path.join(project_root, "file", "v1.mp4")
    audio_path = os.path.join(project_root, "file", "v1.mp3")
    
    # 设置输出文件路径
    output_dir = os.path.join(project_root, "file", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "v1_mixed.mp4")
    
    try:
        # 执行视频音频混合
        result_path = mix_video_audio(video_path, audio_path, output_path)
        print(f"✅ 视频音频混合成功！输出文件：{result_path}")
        
        # 验证输出文件是否存在
        assert os.path.exists(result_path), "输出文件不存在"
        assert os.path.getsize(result_path) > 0, "输出文件大小为0"
        
        print("✅ 测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败：{str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试视频音频混合功能...")
    test_mix_video_audio()