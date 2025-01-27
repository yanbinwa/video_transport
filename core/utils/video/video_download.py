import os

import requests
import wget as wget

from core.utils.common.logger import log

video_download_url = "https://tubedown.cn/api/youtube"

audio_format = ["medium, DRC", "medium", "low, DRC", "low"]
video_format = ["1080p", "720p", "480p", "360p", "240p", "144p"]


def download_video_by_url(url, file_path):
    url = get_video_download_url(url)
    download_by_url(url, file_path)


def download_audio_by_url(url, file_path):
    url = get_audio_download_url(url)
    download_by_url(url, file_path)


def get_video_audio_list_download_url(url):
    data = {
        "url": url
    }
    response = requests.post(video_download_url, json=data)
    if response.status_code == 200:
        return response.json()["data"]["formats"]
    else:
        return None


def get_video_download_url(url):
    # 如何判断
    data_list = get_video_audio_list_download_url(url);
    # 如何判断: asr != None and fileSize != None，取fileSize最大的一个作为结果
    data_list = [data for data in data_list if data.get("format_note", None) is None
                 and data.get('format_note') in video_format
                 and data.get("filesize", None) is not None]
    return max(data_list, key=lambda x: x["filesize"])["url"]


def get_audio_download_url(url):
    data_list = get_video_audio_list_download_url(url);
    # 如何判断: asr != None and fileSize != None，取fileSize最大的一个作为结果
    data_list = [data for data in data_list if data.get("asr", None) is not None
                 and data.get('format_note') in audio_format
                 and data.get("filesize", None) is not None]
    return max(data_list, key=lambda x: x["filesize"])["url"]


def download_by_url(url, file_path):
    # 通过代理将url内容下载成file_path
    os.environ['http_proxy'] = 'http://127.0.0.1:33210'
    os.environ['https_proxy'] = 'http://127.0.0.1:33210'
    os.environ['all_proxy'] = 'socks5://127.0.0.1:33211'
    log.info("download url: " + url)
    try:
        if file_path:
            wget.download(url, file_path)
        else:
            wget.download(url)
        print(f"\n文件下载完成")

    except Exception as e:
        print(f"下载失败: {str(e)}")


