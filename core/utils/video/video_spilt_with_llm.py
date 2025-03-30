from typing import List

from dashscope import Generation

from core.utils.video.video_split import time_str_to_seconds

role = """
# 角色
你是一个专业的视频srt字幕分析剪辑器，具备精准分析和高效剪辑视频字幕的能力。能够从输入的视频srt字幕中，深入剖析并提取出精彩且尽可能连续的片段。

## 技能
### 技能 1: 分析剪辑字幕
1. 接收视频的srt字幕作为输入。
2. 仔细分析字幕内容，识别出其中精彩的部分，并确保这些部分在时间上尽可能连续。
3. 将片段中在时间上连续的多个句子及它们的时间戳合并为一条，注意严格确保文字与时间戳的正确匹配。
4. 每个裁剪出的片段时长需控制在1分钟左右。
5. 输出需严格按照如下格式：1. [开始时间-结束时间]，注意其中的连接符是“-”。除了上述格式的时间范围内容以外什么都不要输出。

## 限制:
- 输出内容必须严格按照指定格式。
- 每个片段时长尽量接近1分钟，误差控制在合理范围内。 
"""


# 从llm_response中截取时间范围，并转换成时间范围元组。
def get_time_ranges(llm_response: str) -> List[tuple]:
    time_ranges = []
    for line in llm_response.split('\n'):
        if '[' in line and ']' in line:
            line = line[line.index('['):line.index(']') + 1]
            start_time, end_time = line[1:-1].split('-')
            # 00:00:25,500 格式转换成秒，保留两位小数
            start_time_value = time_str_to_seconds(start_time.strip())
            end_time_value = time_str_to_seconds(end_time.strip())
            time_ranges.append((start_time_value, end_time_value))
    return time_ranges


def srt_spilt_by_llm(srt_content) -> str:
    messages = [
        {'role': 'system', 'content': role},
        {'role': 'user', 'content': srt_content}
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key="sk-14a27b1701374cf3a4c00e9897327467",
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        result_format="message"
    )

    if response.status_code == 200:
        return response.output.choices[0].message.content
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        raise Exception(f"HTTP返回码：{response.status_code}")


def srt_spilt_by_llm_v2(srt_file_path) -> List[tuple]:
    # 从文件中读取字符串
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    return srt_spilt_by_llm(srt_content)
