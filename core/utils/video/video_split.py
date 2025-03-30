################################################################################
# 视频切分，识别视频转场
################################################################################

import os
from typing import List

from moviepy.editor import VideoFileClip
from tqdm import tqdm

from .scene_detection_methods import (
    detect_by_frame_diff,
    detect_by_histogram,
    detect_by_optical_flow,
    detect_combined
)
from ..common.logger import log


def detect_scene_changes(video_path: str, threshold: float = 30.0, method: str = 'frame_diff') -> List[float]:
    """
    检测视频中的转场时间点
    
    Args:
        video_path: 视频文件路径
        threshold: 判断转场的阈值，值越大检测越不敏感
        method: 检测方法，可选值：
               - 'frame_diff': 帧差法（默认）
               - 'histogram': 直方图比较法
               - 'optical_flow': 光流法
               - 'combined': 组合方法
        
    Returns:
        转场时间点列表（以秒为单位）
    """
    # 根据方法选择相应的检测函数
    if method == 'frame_diff':
        return detect_by_frame_diff(video_path, threshold)
    elif method == 'histogram':
        return detect_by_histogram(video_path, threshold)
    elif method == 'optical_flow':
        return detect_by_optical_flow(video_path, threshold)
    elif method == 'combined':
        return detect_combined(video_path, threshold, threshold)
    else:
        raise ValueError(f"不支持的检测方法: {method}")


def split_video(video_path: str, output_dir: str, scene_changes: List[float], min_duration: float = 10.0) -> List[str]:
    """
    根据检测到的转场点切分视频
    
    Args:
        video_path: 源视频路径
        output_dir: 输出目录
        scene_changes: 转场时间点列表
        min_duration: 最小视频时长（秒），小于这个时长的片段会被合并
        
    Returns:
        切分后的视频文件路径列表
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 清空输出目录
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # 使用 moviepy 加载视频
    video = VideoFileClip(video_path)
    
    # 添加视频起始点和结束点
    time_points = [0] + scene_changes + [video.duration]
    
    # 合并过短的片段
    merged_points = []
    i = 0
    while i < len(time_points) - 1:
        start_time = time_points[i]
        end_time = time_points[i + 1]
        duration = end_time - start_time
        
        # 如果当前片段太短，尝试与下一个片段合并
        if duration < min_duration and i + 2 < len(time_points):
            next_end_time = time_points[i + 2]
            merged_duration = next_end_time - start_time
            # 如果合并后的时长仍然小于最小时长，继续尝试合并下一个片段
            while merged_duration < min_duration and i + 3 < len(time_points):
                i += 1
                next_end_time = time_points[i + 2]
                merged_duration = next_end_time - start_time
            merged_points.append(start_time)
            i += 2
        else:
            merged_points.append(start_time)
            i += 1
    
    # 添加最后的结束点
    merged_points.append(time_points[-1])
    
    output_files = []
    # 按照合并后的时间点切分视频
    for i in tqdm(range(len(merged_points) - 1), desc="按照时间点切分视频", position=0):
        start_time = merged_points[i]
        end_time = merged_points[i + 1]
        
        # 设置输出文件
        output_path = os.path.join(output_dir, f"scene_{i:03d}.mp4")
        # 设置首帧图片保存路径
        thumbnail_path = os.path.join(output_dir, f"scene_{i:03d}_thumb.jpg")
        
        # 提取视频片段
        clip = video.subclip(start_time, end_time)
        
        # 保存视频片段（保留音频）
        try:
            # 确保当前目录可写
            temp_dir = os.path.dirname(output_path)
            os.makedirs(temp_dir, exist_ok=True)
            
            # 设置临时文件路径
            temp_audio_path = os.path.join(temp_dir, f'temp_audio_{i}.m4a')
            
            # 先检查视频是否有音频
            has_audio = clip.audio is not None
            
            # 设置 ffmpeg_params 来避免 stdout 错误
            ffmpeg_params = ['-hide_banner', '-loglevel', 'error']
            
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac' if has_audio else None,
                temp_audiofile=temp_audio_path if has_audio else None,
                remove_temp=True,
                verbose=False,
                logger=None,
                ffmpeg_params=ffmpeg_params,
                preset='medium',  # 使用更稳定的编码预设
                threads=2  # 限制线程数以提高稳定性
            )
            
        except Exception as e:
            log.error(f"保存视频片段时出错: {str(e)}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise
        
        # 保存首帧缩略图
        clip.save_frame(thumbnail_path, t=0)
        
        # 关闭当前片段
        clip.close()
        
        output_files.append(output_path)
    
    # 关闭原视频
    video.close()
    
    return output_files


def split_video_v2(video_path: str, output_dir: str, time_ranges: List[tuple]) -> List[str]:
    """
    根据指定的时间区间列表切分视频
    
    Args:
        video_path: 源视频路径
        output_dir: 输出目录
        time_ranges: 时间区间列表，每个元素是一个元组 (start_time, end_time)
                    例如: [(0, 10), (15, 25), (30, 40)] 表示提取 0-10秒、1-25秒和30-40秒的片段
        
    Returns:
        切分后的视频文件路径列表
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 使用 moviepy 加载视频
    video = VideoFileClip(video_path)
    
    output_files = []
    # 按照时间区间切分视频
    for i, (start_time, end_time) in enumerate(tqdm(time_ranges, desc="按照时间区间切分视频", position=0)):
        # 验证时间区间
        if start_time >= end_time:
            print(f"\n警告: 跳过无效的时间区间 [{start_time}, {end_time}]")
            continue
        
        if start_time < 0 or end_time > video.duration:
            print(f"\n警告: 时间区间 [{start_time}, {end_time}] 超出视频范围 [0, {video.duration}]")
            continue
        
        # 设置输出文件
        output_path = os.path.join(output_dir, f"clip_{i:03d}_{start_time:.1f}-{end_time:.1f}.mp4")
        # 设置首帧图片保存路径
        thumbnail_path = os.path.join(output_dir, f"clip_{i:03d}_{start_time:.1f}-{end_time:.1f}_thumb.jpg")
        
        # 提取视频片段
        try:
            clip = video.subclip(start_time, end_time)
            
            # 确保当前目录可写
            temp_dir = os.path.dirname(output_path)
            os.makedirs(temp_dir, exist_ok=True)
            
            # 设置临时文件路径
            temp_audio_path = os.path.join(temp_dir, f'temp_audio_{i}.m4a')
            
            # 先检查视频是否有音频
            has_audio = clip.audio is not None
            
            # 设置 ffmpeg_params 来避免 stdout 错误
            ffmpeg_params = ['-hide_banner', '-loglevel', 'error']
            
            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac' if has_audio else None,
                temp_audiofile=temp_audio_path if has_audio else None,
                remove_temp=True,
                verbose=False,
                logger=None,
                ffmpeg_params=ffmpeg_params,
                preset='medium',  # 使用更稳定的编码预设
                threads=2  # 限制线程数以提高稳定性
            )
            
            # 保存首帧缩略图
            clip.save_frame(thumbnail_path, t=0)
            
            # 关闭当前片段
            # clip.close()
            
            output_files.append(output_path)
            
        except Exception as e:
            log.error(f"保存视频片段时出错: {str(e)}")
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except:
                    pass
            raise
    
    # 关闭原视频
    video.close()
    
    return output_files


def detect_scene_and_spilt(video_path: str, output_dir: str, threshold: float = 30.0, min_duration: float = 30.0):
    """
    检测视频转场并切分视频
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
        threshold: 判断转场的阈值，值越大检测越不敏感
        min_duration: 最小视频时长（秒）
    """
    # 检测转场
    scene_changes = detect_scene_changes(video_path, threshold)

    # 切分视频
    return split_video(video_path, output_dir, scene_changes, min_duration)


def time_str_to_seconds(time_str: str) -> float:
    """
    将时间字符串转换为秒数（保留2位小数）
    
    Args:
        time_str: 时间字符串，格式为 "HH:MM:SS,mmm" 或 "HH:MM:SS.mmm"
                 例如: "00:04:59,879" 或 "00:04:59.879"
    
    Returns:
        float: 转换后的秒数
        
    Examples:
        >>> time_str_to_seconds("00:04:59,879")
        299.88
        >>> time_str_to_seconds("01:00:00,000")
        3600.00
    """
    # 统一将逗号替换为点
    time_str = time_str.replace(',', '.')
    
    try:
        # 分割时、分、秒
        hours, minutes, seconds = time_str.split(':')
        
        # 转换为数字
        hours = int(hours)
        minutes = int(minutes)
        # 秒可能包含小数点，所以用 float
        seconds = float(seconds)
        
        # 计算总秒数
        total_seconds = hours * 3600 + minutes * 60 + seconds
        
        # 保留2位小数
        return round(total_seconds, 2)
        
    except ValueError as e:
        raise ValueError(f"时间格式错误，应为 'HH:MM:SS,mmm' 或 'HH:MM:SS.mmm'，实际输入: {time_str}")