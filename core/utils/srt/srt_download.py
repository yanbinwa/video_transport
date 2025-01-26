import base64
import json
import re
from logging import log

import requests
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad


# 需要登录态才能获取字幕的url
def get_org_bilibili_subtitle(url):
    # 提取视频ID
    video_id = ""
    patterns = [
        r'BV\w+',
        r'av\d+',
        r'/video/(BV\w+)',
        r'/video/av(\d+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group()
            break

    if not video_id:
        raise ValueError("无法从URL中提取视频ID")

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    # 获取视频信息
    api_url = f"https://api.bilibili.com/x/player/v2?bvid={video_id}" if video_id.startswith('BV') else f"https://api.bilibili.com/x/player/v2?aid={video_id[2:]}"
    response = requests.get(api_url, headers=headers)
    data = response.json()

    if data['code'] != 0:
        raise Exception(f"获取字幕信息失败: {data['message']}")

    # 获取字幕URL
    subtitle_list = data['data']['subtitle']['subtitles']
    if not subtitle_list:
        return "该视频没有字幕"

    subtitle_url = "https:" + subtitle_list[0]['subtitle_url']

    # 下载字幕内容
    response = requests.get(subtitle_url, headers=headers)
    subtitle_data = response.json()

    # 提取字幕文本
    subtitles = []
    for item in subtitle_data['body']:
        subtitles.append(item['content'])

    return "\n".join(subtitles)


def get_bilibili_subtitle(url):
    api_url = 'https://www.kedou.life/api/video/subtitleExtract'
    key = 'kedou@8989!63239'
    iv = base64.b64decode('a2Vkb3VAODk4OSE2MzIzMw==')
    public_key = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJZWIUIje8VjJ3okESY8stCs/a95hTUqK3fD/AST0F8mf7rTLoHCaW+AjmrqVR9NM/tvQNni67b5tGC5z3PD6oROJJ24QfcAW9urz8WjtrS/pTAfGeP/2AMCZfCu9eECidy16U2oQzBl9Q0SPoz0paJ9AfgcrHa0Zm3RVPL7JvOUzscL4AnirYImPsdaHZ52hAwz5y9bYoiWzUkuG7LvnAxO6JHQ71B3VTzM3ZmstS7wBsQ4lIbD318b49x+baaXVmC3yPW/E4Ol+OBZIBMWhzl7FgwIpgbGmsJSsqrOq3D8IgjS12K5CgkOT7EB/sil7lscgc22E5DckRpMYRG8dwIDAQAB"""

    # AES 加密
    data = json.dumps({"url": url}).encode('utf-8')
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    aes_encrypted = base64.b64encode(cipher.encrypt(padded_data)).decode('utf-8')

    # RSA 加密
    rsa_key = RSA.importKey(base64.b64decode(public_key))
    cipher_rsa = PKCS1_v1_5.new(rsa_key)
    encrypted_data = base64.b64encode(cipher_rsa.encrypt(aes_encrypted.encode())).decode('utf-8')

    # 发送请求
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com'
    }

    try:
        response = requests.post(api_url, data=encrypted_data, headers=headers)
        data = response.json()

        if (data.get('data') and
            data['data'].get('subtitleItemVoList') and
            len(data['data']['subtitleItemVoList']) > 0):

            subtitles = data['data']['subtitleItemVoList'][0]['content']
            if not subtitles:
                log.error("字幕为空")
                return None
            return subtitles
        else:
            log.error("data is empty")
            return None

    except Exception as error:
        log.error(f"获取字幕时出错: {str(error)}")
        return None
