import re
from datetime import datetime

from funasr import AutoModel

template = '{}\n{} --> {}\n{}\n\n'
model_dir = "paraformer-zh"


def generate_srt_file_by_audio(audio_path, file_path):
    sentence_info = extract_srt_from_audio(audio_path)
    return generate_srt_file(sentence_info, file_path)


def extract_srt_from_audio(audio_path):
    model = AutoModel(model=model_dir, vad_model="fsmn-vad", punc_model="ct-punc", spk_model="cam++")
    res = model.generate(input=audio_path, batch_size_s=1, hotword='魔搭')
    return res[0]["sentence_info"]


def generate_srt_file(sentence_info, file_path):
    if len(sentence_info) <= 0:
        return False

    result = ''
    for i, sentence in enumerate(sentence_info):
        result = result + template.format(i + 1, timestamp_to_srt(sentence["start"]),
                                          timestamp_to_srt(sentence["end"]), trim_sentence(sentence["text"]))

    # 将result写入到srt文件中
    with open(file_path, 'w') as f:
        f.write(result)
    return True


def generate_srt_file_by_subtitle(subtitles, file_path):
    if len(subtitles) <= 0:
        return False

    result = ''
    for i, subtitle in enumerate(subtitles):
        result = result + template.format(i + 1, timestamp_to_srt(subtitle["start"] * 1000),
                                          timestamp_to_srt((subtitle["start"] + subtitle["duration"]) * 1000), trim_sentence(subtitle["text"]))

    # 将result写入到srt文件中
    with open(file_path, 'w') as f:
        f.write(result)
    return True


# 10:03:40,000 --> 11:02:35,000
def get_subtitle_from_srt(srt_file_path, start_second, end_second):
    with open(srt_file_path, 'r') as f:
        lines = f.readlines()
        subtitles = []
        for i in range(0, len(lines), 4):
            if i + 2 >= len(lines):
                print("invalid srt")
                break
            time_str = lines[i + 1].split('-->')[0]
            time_second = parse_time(time_str)
            if time_second < start_second:
                continue
            elif time_second < end_second:
                subtitles.append(lines[i + 2])
            else:
                break
        if len(subtitles) == 0:
            return ''
        return ' '.join(subtitles)


# 将timestamp转换中srt中的时间格式
def timestamp_to_srt(timestamp):
    second = round(timestamp // 1000)
    hours = round(second // 3600)
    minutes = round((second % 3600) // 60)
    seconds = round(second % 60)
    milliseconds = round(timestamp % 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def trim_sentence(sentence):
    # 去除句子开头和结尾的空格和换行符
    sentence = sentence.strip()
    # 去除句子中的多个空格和换行符
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence


def parse_time(time_str: str) -> int:
    """
    将 SRT 时间格式转换为秒数

    Args:
        time_str: SRT格式的时间字符串 (00:00:00,000)

    Returns:
        float: 转换后的秒数
    """
    # 将逗号替换为点，以便解析毫秒
    time_str = time_str.replace(',', '.')
    time_str = time_str.replace(' ', '')
    time_obj = datetime.strptime(time_str, '%H:%M:%S.%f')
    return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second

