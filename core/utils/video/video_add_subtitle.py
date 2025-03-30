"""
为视频添加字幕
"""
import os
from typing import Optional

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from tqdm import tqdm

from ..common.logger import log


def get_system_font():
    """
    获取系统中文字体路径
    """
    # 常见的中文字体路径
    font_paths = [
        # macOS
        '/System/Library/Fonts/PingFang.ttc',  # PingFang
        '/System/Library/Fonts/STHeiti Light.ttc',  # Heiti
        '/System/Library/Fonts/STHeiti Medium.ttc',
        # Windows
        'C:\\Windows\\Fonts\\msyh.ttc',  # Microsoft YaHei
        'C:\\Windows\\Fonts\\simhei.ttf',  # SimHei
        # Linux
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    ]
    
    # 检查字体文件是否存在
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    
    # 如果找不到中文字体，返回默认字体
    return 'Arial'


def add_subtitle(video_path: str,
                srt_path: str,
                output_path: Optional[str] = None,
                font: str = None,
                fontsize: int = 24,
                color: str = 'white',
                stroke_color: str = 'black',
                stroke_width: float = 1.0) -> str:
    """
    为视频添加字幕
    
    Args:
        video_path: 视频文件路径
        srt_path: SRT字幕文件路径
        output_path: 输出文件路径，如果不指定则在原文件名后添加"_with_subtitle"
        font: 字体，如果不指定则自动选择系统中文字体
        fontsize: 字体大小
        color: 字体颜色
        stroke_color: 描边颜色
        stroke_width: 描边宽度
        
    Returns:
        str: 添加字幕后的视频文件路径
    """
    try:
        # 如果没有指定字体，使用系统中文字体
        if font is None:
            font = get_system_font()
            log.info(f"使用系统字体: {font}")
        
        # 加载视频
        video = VideoFileClip(video_path)
        
        # 加载字幕
        subs = pysrt.open(srt_path)
        
        # 生成字幕剪辑
        subtitle_clips = []
        
        for sub in tqdm(subs, desc="处理字幕"):
            start_time = sub.start.ordinal / 1000  # 转换为秒
            end_time = sub.end.ordinal / 1000
            duration = end_time - start_time
            
            try:
                # 创建文本剪辑
                text_clip = (TextClip(sub.text,
                                    fontsize=fontsize,
                                    font=font,
                                    color=color,
                                    stroke_color=stroke_color,
                                    stroke_width=stroke_width,
                                    size=(video.w * 0.8, None),  # 宽度设为视频宽度的80%
                                    method='caption')
                            .set_position(('center', 'bottom'))  # 设置位置在底部居中
                            .set_duration(duration)
                            .set_start(start_time))
                subtitle_clips.append(text_clip)
            except Exception as e:
                log.error(f"处理字幕时出错: {str(e)}, 字幕内容: {sub.text}")
                continue
        
        # 合成视频
        final_video = CompositeVideoClip([video] + subtitle_clips)
        
        # 如果没有指定输出路径，在原文件名后添加"_with_subtitle"
        if output_path is None:
            file_dir = os.path.dirname(video_path)
            file_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(file_dir, f"{file_name}_with_subtitle.mp4")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存视频
        final_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None,
            ffmpeg_params=['-hide_banner', '-loglevel', 'error']
        )
        
        # 关闭视频
        video.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        log.error(f"添加字幕时出错: {str(e)}")
        raise

