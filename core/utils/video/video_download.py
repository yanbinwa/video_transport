import os
import subprocess

import requests
import wget as wget

from core.utils.common.logger import log

video_download_url = "https://tubedown.cn/api/ytdlp"

audio_format = ["medium, DRC", "medium", "low, DRC", "low"]
video_format = ["1080p", "720p", "480p", "360p", "240p", "144p", "1080p60", "720p60", "480p60", "360p60",
                "240p60", "144p60"]


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
    data_list = [data for data in data_list if data.get("format_note", None) is not None
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
    
    wget_cmd = [
        'wget',
        url,
        '-O', file_path,
        '--progress=bar:force',  # 强制显示进度条
        '--show-progress',       # 显示详细进度信息
        '-q'                     # 不显示 wget 的其他输出信息
    ]
    
    try:
        process = subprocess.Popen(
            wget_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 在同一行更新进度
        for line in process.stderr:
            print(f"\r{line.strip()}", end='', flush=True)
        print()  # 下载完成后换行
            
        process.wait()
        return True if process.returncode == 0 else False
    except Exception as e:
        print(f"\r下载出错: {str(e)}")
        return False


