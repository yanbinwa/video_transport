import re
from typing import List, Dict, Optional

from youtube_transcript_api import YouTubeTranscriptApi


def get_subtitles(video_id: str, languages: List[str] = ['en', 'zh', 'zh-CN']) -> Dict:
    """获取指定语言的字幕"""
    try:
        # 获取所有可用字幕
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        results = {}
        for lang in languages:
            try:
                # 尝试获取指定语言的字幕
                transcript = transcript_list.find_transcript([lang])
                subtitles = transcript.fetch()

                # 格式化字幕数据
                formatted_subs = []
                for sub in subtitles:
                    formatted_subs.append({
                        'start': sub['start'],
                        'duration': sub['duration'],
                        'text': sub['text']
                    })

                results[lang] = formatted_subs

            except Exception as e:
                print(f"获取{lang}字幕失败: {str(e)}")
                continue

        return results

    except Exception as e:
        print(f"获取字幕失败: {str(e)}")
        return {}


def extract_video_id(url: str) -> Optional[str]:
    """从YouTube URL中提取视频ID"""
    try:
        # 处理不同格式的YouTube URL
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # 标准和分享链接
            r'youtu\.be\/([0-9A-Za-z_-]{11})',  # 短链接
            r'^([0-9A-Za-z_-]{11})$'  # 直接是视频ID
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    except Exception as e:
        print(f"提取视频ID失败: {str(e)}")
        return None


def convert_subtitles(subtitles) -> str:
    return "\n".join([sub['text'] for sub in subtitles])


def process_video_srt(url: str, languages: List[str] = ['en', 'zh-Hans']) -> str:
    """处理单个视频"""
    try:
        # 提取视频ID
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("无效的YouTube URL")

        # 获取字幕
        subtitles = get_subtitles(video_id, languages)
        if not subtitles:
            raise ValueError("未找到字幕")

        return subtitles

    except Exception as e:
        print(f"处理视频失败: {str(e)}")
        return {}


def process_video(url: str, languages: List[str] = ['en', 'zh-Hans']) -> str:
    subtitles = process_video_srt(url, languages)
    # 优先选择中文字幕，如果找不到，则选择英文字幕
    if 'zh-Hans' in subtitles:
        return convert_subtitles(subtitles['zh-Hans'])
    elif 'en' in subtitles:
        return convert_subtitles(subtitles['en'])
    else:
        raise ValueError("未找到可用的字幕")
