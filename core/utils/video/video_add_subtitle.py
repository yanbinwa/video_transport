import os

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


def add_subtitle_to_video(video_path: str, srt_path: str, output_path: str, 
                         fontsize: int = 24, 
                         font: str = 'Arial',
                         color: str = 'white',
                         stroke_color: str = 'black',
                         stroke_width: int = 1,
                         y_position: float = 0.85) -> str:
    """
    将 SRT 字幕文件添加到视频中
    
    Args:
        video_path (str): 视频文件路径
        srt_path (str): SRT 字幕文件路径
        output_path (str): 输出文件路径
        fontsize (int): 字体大小，默认 24
        font (str): 字体名称，默认 Arial
        color (str): 字体颜色，默认白色
        stroke_color (str): 描边颜色，默认黑色
        stroke_width (int): 描边宽度，默认 1
        y_position (float): 字幕的垂直位置，范围从0到1，0表示顶部，1表示底部，默认 0.85
        
    Returns:
        str: 输出文件的路径
    """
    try:
        # 加载视频文件
        video = VideoFileClip(video_path)

        # 加载字幕文件
        subs = pysrt.open(srt_path)

        # 创建字幕剪辑列表
        subtitle_clips = []

        for sub in subs:
            # 转换时间为秒
            start_time = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + sub.start.milliseconds / 1000
            end_time = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + sub.end.milliseconds / 1000
            duration = end_time - start_time

            # 创建文本剪辑
            text_clip = (TextClip(sub.text,
                                  fontsize=fontsize,
                                  font=font,
                                  color=color,
                                  stroke_color=stroke_color,
                                  stroke_width=stroke_width,
                                  size=(video.w * 0.8, None),  # 宽度设为视频宽度的80%
                                  method='caption')
                         .set_position(('center', y_position))  # 设置位置
                         .set_duration(duration)
                         .set_start(start_time))

            subtitle_clips.append(text_clip)

        # 合成带字幕的视频
        final_video = CompositeVideoClip([video] + subtitle_clips)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 写入新的视频文件
        final_video.write_videofile(output_path,
                                    codec='libx264',
                                    audio_codec='aac',
                                    temp_audiofile='temp-audio.m4a',
                                    remove_temp=True)

        # 关闭文件以释放资源
        video.close()
        final_video.close()

        return output_path

    except Exception as e:
        raise Exception(f"添加字幕时出错: {str(e)}")

