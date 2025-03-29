from core.utils.common.logger import log
from core.utils.srt.srt_download_impl import bilibili
from core.utils.srt.srt_download_impl import youtube
from core.utils.srt.srt_generate import generate_srt_file_by_subtitle


def get_subtitle(url):
    platform = get_platform_from_url(url)
    if platform is None:
        return None
    if platform == 'bilibili':
        return bilibili.get_bilibili_subtitle(url)
    elif platform == 'youtube':
        return youtube.process_video(url=url, languages=['en', 'zh-Hans'])


def get_srt_file(url, file_path, languages=['en', 'zh-Hans']):
    platform = get_platform_from_url(url)
    if platform is None:
        return None
    if platform == 'bilibili':
        return None
    elif platform == 'youtube':
        srt_map = youtube.process_video_srt(url=url, languages=languages)
        if srt_map is None:
            return None
        for lan in languages:
            if lan in srt_map:
                generate_srt_file_by_subtitle(srt_map[lan], file_path)


def get_platform_from_url(url):
    if 'www.youtube.com' in url:
        return 'youtube'
    elif 'www.bilibili.com' in url:
        return 'bilibili'
    else:
        log.error("为止链接：" + url)
        return None
