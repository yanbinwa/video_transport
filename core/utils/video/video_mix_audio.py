import os
from moviepy.editor import VideoFileClip, AudioFileClip


def mix_video_audio(video_path: str, audio_path: str, output_path: str) -> str:
    """
    将视频和音频文件混合成一个新的视频文件
    
    Args:
        video_path (str): 视频文件路径
        audio_path (str): 音频文件路径
        output_path (str): 输出文件路径
        
    Returns:
        str: 输出文件的路径
    """
    try:
        # 加载视频文件
        video = VideoFileClip(video_path)
        
        # 加载音频文件
        audio = AudioFileClip(audio_path)
        
        # 如果音频长度超过视频长度，将音频裁剪至视频长度
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        
        # 将音频设置到视频中
        final_video = video.set_audio(audio)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入新的视频文件
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        # 关闭文件以释放资源
        video.close()
        audio.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        raise Exception(f"混合视频和音频时出错: {str(e)}")
