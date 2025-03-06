from core.utils.common.logger import log
from core.utils.srt.srt_download_impl import bilibili
from core.utils.srt.srt_download_impl import youtube


def get_subtitle(url):
    platform = get_platform_from_url(url)
    if platform is None:
        return None
    if platform == 'bilibili':
        return bilibili.get_bilibili_subtitle(url)
    elif platform == 'youtube':
        return youtube.process_video(url=url, languages=['en', 'zh-Hans'])


def get_platform_from_url(url):
    if 'www.youtube.com' in url:
        return 'youtube'
    elif 'www.bilibili.com' in url:
        return 'bilibili'
    else:
        log.error("为止链接：" + url)
        return None
