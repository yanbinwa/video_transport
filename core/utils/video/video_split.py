################################################################################
# 视频切分，识别视频转场
################################################################################

from typing import List
from tqdm import tqdm

import cv2
import numpy as np


def detect_scene_changes(video_path: str, threshold: float = 30.0) -> List[float]:
    """
    检测视频中的转场时间点
    
    Args:
        video_path: 视频文件路径
        threshold: 判断转场的阈值，值越大检测越不敏感
        
    Returns:
        转场时间点列表（以秒为单位）
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_frame = None
    scene_changes = []
    
    # 使用tqdm创建进度条
    for frame_count in tqdm(range(total_frames), desc="检测视频转场"):
        ret, frame = cap.read()
        if not ret:
            break
            
        # 转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            # 计算帧间差异
            diff = cv2.absdiff(gray, prev_frame)
            mean_diff = np.mean(diff)
            
            # 如果差异大于阈值，认为是转场点
            if mean_diff > threshold:
                time_point = frame_count / fps
                scene_changes.append(time_point)
        
        prev_frame = gray
    
    cap.release()
    return scene_changes


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
    import os
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 清空输出目录
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    
    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 添加视频起始点和结束点
    time_points = [0] + scene_changes + [total_frames / fps]
    
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
    for i in tqdm(range(len(merged_points) - 1), desc="按照时间点切分视频"):
        start_time = merged_points[i]
        end_time = merged_points[i + 1]
        
        # 计算起始和结束帧
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)
        
        # 设置输出文件
        output_path = os.path.join(output_dir, f"scene_{i:03d}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 定位到起始帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # 写入帧
        for _ in range(start_frame, end_frame):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
        out.release()
        output_files.append(output_path)
    
    cap.release()
    return output_files


def detect_scene_and_spilt(video_path: str, output_dir: str):
    # 检测转场
    scene_changes = detect_scene_changes(video_path, threshold=30.0)

    # 切分视频
    split_video(video_path, output_dir, scene_changes)
