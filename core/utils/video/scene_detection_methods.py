from typing import List
import cv2
import numpy as np
from tqdm import tqdm


def detect_by_frame_diff(video_path: str, threshold: float = 30.0) -> List[float]:
    """
    使用帧差法检测场景变化
    优点：计算简单，速度快
    缺点：对渐变场景不敏感
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_frame = None
    scene_changes = []
    
    for frame_count in tqdm(range(total_frames), desc="检测视频转场-帧差法", position=0):
        ret, frame = cap.read()
        if not ret:
            break
            
        # 转换为灰度图并进行高斯模糊，减少噪声
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
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


def detect_by_histogram(video_path: str, threshold: float = 0.5) -> List[float]:
    """
    使用直方图比较法检测场景变化
    优点：对光照变化不敏感
    缺点：可能会漏检一些细微的场景变化
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_hist = None
    scene_changes = []
    
    for frame_count in tqdm(range(total_frames), desc="检测视频转场-直方图法", position=0):
        ret, frame = cap.read()
        if not ret:
            break
            
        # 计算HSV颜色空间的直方图
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        
        if prev_hist is not None:
            # 计算直方图相似度
            similarity = cv2.compareHist(hist, prev_hist, cv2.HISTCMP_CORREL)
            
            # 如果相似度低于阈值，认为是转场点
            if similarity < threshold:
                time_point = frame_count / fps
                scene_changes.append(time_point)
        
        prev_hist = hist
    
    cap.release()
    return scene_changes


def detect_by_optical_flow(video_path: str, threshold: float = 0.3) -> List[float]:
    """
    使用光流法检测场景变化
    优点：可以检测运动变化，对渐变场景敏感
    缺点：计算量较大
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("无法打开视频文件")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    prev_frame = None
    scene_changes = []
    
    # ShiTomasi 角点检测参数
    feature_params = dict(maxCorners=100,
                         qualityLevel=0.3,
                         minDistance=7,
                         blockSize=7)
    
    # Lucas-Kanade 光流参数
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    for frame_count in tqdm(range(total_frames), desc="检测视频转场-光流法", position=0):
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if prev_frame is not None:
            # 检测特征点
            p0 = cv2.goodFeaturesToTrack(prev_frame, mask=None, **feature_params)
            
            if p0 is not None:
                # 计算光流
                p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame, gray, p0, None, **lk_params)
                
                if p1 is not None:
                    # 选择好的点
                    good_new = p1[st==1]
                    good_old = p0[st==1]
                    
                    # 计算点的平均移动距离
                    if len(good_new) > 0 and len(good_old) > 0:
                        distances = np.sqrt(np.sum((good_new - good_old) ** 2, axis=1))
                        avg_movement = np.mean(distances)
                        
                        # 如果平均移动距离大于阈值，认为是转场点
                        if avg_movement > threshold:
                            time_point = frame_count / fps
                            scene_changes.append(time_point)
        
        prev_frame = gray
    
    cap.release()
    return scene_changes


def detect_combined(video_path: str, 
                   frame_diff_threshold: float = 30.0,
                   hist_threshold: float = 0.5) -> List[float]:
    """
    组合多种方法检测场景变化
    优点：结合多种方法的优势，检测更准确
    缺点：计算量增加
    """
    # 获取各种方法的结果
    frame_diff_scenes = detect_by_frame_diff(video_path, frame_diff_threshold)
    hist_scenes = detect_by_histogram(video_path, hist_threshold)
    
    # 合并结果
    all_scenes = sorted(set(frame_diff_scenes + hist_scenes))
    
    # 合并相近的时间点（比如1秒内的多个检测点）
    merged_scenes = []
    if all_scenes:
        current_scene = all_scenes[0]
        for scene in all_scenes[1:]:
            if scene - current_scene > 1.0:  # 如果间隔大于1秒
                merged_scenes.append(current_scene)
                current_scene = scene
            else:
                # 取平均值
                current_scene = (current_scene + scene) / 2
        merged_scenes.append(current_scene)
    
    return merged_scenes