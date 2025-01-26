import re
from funasr import AutoModel


template = '{}\n{} --> {}\n{}\n'
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


# 将timestamp转换中srt中的时间格式
def timestamp_to_srt(timestamp):
    hours = timestamp // 3600
    minutes = (timestamp % 3600) // 60
    seconds = timestamp % 60
    milliseconds = (timestamp % 1) * 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def trim_sentence(sentence):
    # 去除句子开头和结尾的空格和换行符
    sentence = sentence.strip()
    # 去除句子中的多个空格和换行符
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence



