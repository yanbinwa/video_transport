'''
将整体流程串联起来
0. 解析youtube视频ID，创建一个文件夹
1. 下载视频，将视频命名为v1.mp4
2. 判断视频是否有音频，如果没有，下载音频，命名为v1.mp3，将视频和音频合并，合并的视频命名为v1_mixed.mp4
3. 下载字幕，命名为v1.srt
4. 通过大模型生成分段，将返回结果写入到llm.txt文件中
5. 分割视频，写入到output/spilt文件夹中
'''

import os
import warnings
from typing import Optional, List, Tuple

from moviepy.editor import VideoFileClip

from core.utils.common.logger import log
from core.utils.srt.srt_download import get_srt_file
from core.utils.srt.srt_download_impl.youtube import extract_video_id
from core.utils.video.video_add_subtitle import add_subtitle
from core.utils.video.video_download import download_video_by_url, download_audio_by_url
from core.utils.video.video_mix_audio import mix_video_audio
from core.utils.video.video_spilt_with_llm import srt_spilt_by_llm_v2, get_time_ranges
from core.utils.video.video_split import split_video_v2
from core.utils.video.video_srt_transfer import translate_srt_file

# 过滤 imageio 的警告
warnings.filterwarnings('ignore', category=DeprecationWarning, module='imageio')
warnings.filterwarnings('ignore', category=UserWarning, module='moviepy')


def suppress_warnings(func):
    """装饰器：用于抑制特定的警告"""

    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=DeprecationWarning, module='imageio')
            warnings.filterwarnings('ignore', category=UserWarning, module='moviepy')
            return func(*args, **kwargs)

    return wrapper


class ProcessState:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.video_path = os.path.join(output_dir, "v1.mp4")
        self.audio_path = os.path.join(output_dir, "v1.mp3")
        self.mixed_path = os.path.join(output_dir, "v1_mixed.mp4")
        self.srt_path = os.path.join(output_dir, "v1.srt")
        self.srt_zh_path = os.path.join(output_dir, "v1_zh-cn.srt")  # 添加中文字幕路径
        self.llm_spilt_path = os.path.join(output_dir, "llm_spilt.txt")  # 大模型切分后的结果
        self.with_subtitle_path = os.path.join(output_dir, "v1_with_subtitle.mp4")
        self.split_dir = os.path.join(output_dir, "output", "split")

    def has_video(self) -> bool:
        """检查视频是否已下载"""
        return os.path.exists(self.video_path) and os.path.getsize(self.video_path) > 0

    def has_audio(self) -> bool:
        """检查音频是否已下载"""
        return os.path.exists(self.audio_path) and os.path.getsize(self.audio_path) > 0

    def has_mixed_video(self) -> bool:
        """检查合并后的视频是否存在"""
        return os.path.exists(self.mixed_path) and os.path.getsize(self.mixed_path) > 0

    def has_subtitle(self) -> bool:
        """检查字幕是否已下载"""
        return os.path.exists(self.srt_path) and os.path.getsize(self.srt_path) > 0

    def has_zh_subtitle(self) -> bool:
        """检查中文字幕是否存在"""
        return os.path.exists(self.srt_zh_path) and os.path.getsize(self.srt_zh_path) > 0

    def has_with_subtitle(self) -> bool:
        """检查字幕已添加到视频中"""
        return os.path.exists(self.with_subtitle_path) and os.path.getsize(self.with_subtitle_path) > 0

    def has_llm_spilt(self ) -> bool:
        """检查大模型切分后的结果是否存在"""
        return os.path.exists(self.llm_spilt_path) and os.path.getsize(self.llm_spilt_path) > 0

    def has_split_videos(self) -> bool:
        """检查是否已有切分的视频"""
        return os.path.exists(self.split_dir) and len(os.listdir(self.split_dir)) > 0

    def get_final_video_path(self) -> str:
        """获取最终使用的视频路径"""
        return self.mixed_path if self.has_mixed_video() else self.video_path


@suppress_warnings
def process_youtube_video(
        url: str,
        output_base_dir: str,
        split_ranges: Optional[List[Tuple[float, float]]] = None,
        force_reprocess: bool = False
) -> str:
    """
    处理YouTube视频的完整流程，支持断点续传
    
    Args:
        url: YouTube视频URL
        output_base_dir: 输出基础目录
        split_ranges: 视频切分时间区间列表，每个元素是(开始时间,结束时间)的元组
                    如果为None，则不进行视频切分
        force_reprocess: 是否强制重新处理所有步骤
    
    Returns:
        str: 处理后的视频目录路径
    """
    # 0. 解析视频ID并创建目录
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"无法从URL中提取视频ID: {url}")

    # 创建输出目录
    output_dir = os.path.join(output_base_dir, video_id)
    os.makedirs(output_dir, exist_ok=True)

    # 初始化状态管理器
    state = ProcessState(output_dir)

    try:
        # 1. 下载视频
        if force_reprocess or not state.has_video():
            log.info(f"开始下载视频: {url}")
            download_video_by_url(url, state.video_path)
        else:
            log.info("视频已存在，跳过下载")

        # 2. 检查视频是否有音频，如果没有则下载并合并
        if not state.has_mixed_video():  # 如果没有合并的视频，检查是否需要合并
            video = VideoFileClip(state.video_path)
            needs_audio = video.audio is None
            video.close()

            if needs_audio:
                log.info("视频没有音频，开始处理音频")
                # 下载音频（如果需要）
                if force_reprocess or not state.has_audio():
                    log.info("开始下载音频")
                    download_audio_by_url(url, state.audio_path)
                else:
                    log.info("音频已存在，跳过下载")

                # 合并视频和音频
                log.info("开始合并视频和音频")
                # 执行视频音频混合
                mixed_path = mix_video_audio(state.video_path, state.audio_path, state.mixed_path)
                log.info("完成视频和音频合并")
        else:
            log.info("合并的视频已存在，跳过音频处理")

        # 3. 下载字幕
        if force_reprocess or not state.has_subtitle():
            log.info("开始下载字幕")
            get_srt_file(url, state.srt_path)
        else:
            log.info("字幕已存在，跳过下载")

        # 3.1 翻译字幕
        if force_reprocess or not state.has_zh_subtitle():
            log.info("开始翻译字幕")
            translate_srt_file(state.srt_path, state.srt_zh_path)
        else:
            log.info("中文字幕已存在，跳过翻译")

        # 4. 添加字幕到视频中
        if force_reprocess or not state.has_with_subtitle():
            log.info("开始添加字幕到视频中")
            add_subtitle(
                video_path=state.mixed_path,
                srt_path=state.srt_zh_path,  # 使用中文字幕
                output_path=state.with_subtitle_path,
                fontsize=40,  # 稍微大一点的字体
                color='white',
                stroke_color='white',
                stroke_width=2  # 稍微粗一点的描边
            )
            log.info("完成添加字幕到视频中")
        else:
            log.info("字幕已添加到视频中，跳过字幕添加步骤")

        # 5. 通过大模型切分
        if force_reprocess or not state.has_llm_spilt():
            log.info("开始使用大模型切分视频")
            llm_response = srt_spilt_by_llm_v2(state.srt_path)
            # 将split_ranges写入到state.llm_spilt_path
            with open(state.llm_spilt_path, 'w') as f:
                f.write(llm_response)
            split_ranges = get_time_ranges(llm_response)
            log.info("完成大模型切分视频")
        else:
            # 从state.llm_spilt_path读取llm_response
            with open(state.llm_spilt_path, 'r') as f:
                llm_response = f.read()
            split_ranges = get_time_ranges(llm_response)
            log.info("大模型切分结果已存在，跳过大模型切分步骤")

        # 6. 如果需要切分视频
        if split_ranges:
            if force_reprocess or not state.has_split_videos():
                # 创建切分输出目录
                os.makedirs(state.split_dir, exist_ok=True)

                # 切分视频
                log.info("开始切分视频")
                split_video_v2(state.get_final_video_path(), state.split_dir, split_ranges)
            else:
                log.info("视频已切分，跳过切分步骤")

    except Exception as e:
        log.error(f"处理过程中出错: {str(e)}")
        # 继续抛出异常，但保留已完成的步骤
        raise

    return output_dir
