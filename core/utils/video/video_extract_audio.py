from pydub import AudioSegment
import subprocess
from typing import Optional
import os
from tqdm import tqdm

def extract_audio(
    video_path: str,
    output_path: Optional[str] = None,
    audio_format: str = "mp3",
    audio_bitrate: str = "192k"
) -> str:
    """
    从视频文件中提取音频

    Args:
        video_path: 视频文件路径
        output_path: 输出音频文件路径，如果为None则使用视频文件名作为音频文件名
        audio_format: 输出音频格式，默认为mp3
        audio_bitrate: 音频比特率，默认为192k

    Returns:
        生成的音频文件路径
    """
    # 如果未指定输出路径，则使用视频文件名
    if output_path is None:
        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(video_dir, f"{video_name}.{audio_format}")

    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    try:
        print(f"正在从视频提取音频: {os.path.basename(video_path)}")
        
        # 使用ffmpeg提取音频
        command = [
            'ffmpeg',
            '-i', video_path,  # 输入文件
            '-vn',  # 不处理视频
            '-acodec', 'libmp3lame' if audio_format == 'mp3' else 'pcm_s16le',  # 音频编码器
            '-ab', audio_bitrate,  # 比特率
            '-ar', '44100',  # 采样率
            '-y',  # 覆盖已存在的文件
            output_path
        ]
        
        # 执行命令
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 等待处理完成
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg 错误: {stderr}")
            
        print(f"音频提取完成: {os.path.basename(output_path)}")
        return output_path

    except Exception as e:
        print(f"提取音频时发生错误: {str(e)}")
        raise

def batch_extract_audio(
    video_dir: str,
    output_dir: Optional[str] = None,
    audio_format: str = "mp3"
) -> list[str]:
    """
    批量处理目录中的视频文件，提取音频

    Args:
        video_dir: 视频文件目录
        output_dir: 输出音频文件目录，如果为None则使用视频所在目录
        audio_format: 输出音频格式，默认为mp3

    Returns:
        生成的音频文件路径列表
    """
    # 支持的视频格式
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
    output_files = []

    # 获取所有视频文件
    video_files = [
        f for f in os.listdir(video_dir)
        if f.lower().endswith(video_extensions)
    ]

    for video_file in tqdm(video_files, desc="处理视频文件"):
        video_path = os.path.join(video_dir, video_file)
        if output_dir:
            # 使用指定的输出目录
            audio_name = os.path.splitext(video_file)[0] + f".{audio_format}"
            output_path = os.path.join(output_dir, audio_name)
        else:
            output_path = None

        try:
            audio_path = extract_audio(video_path, output_path, audio_format)
            output_files.append(audio_path)
        except Exception as e:
            print(f"处理 {video_file} 时发生错误: {str(e)}")
            continue

    return output_files
