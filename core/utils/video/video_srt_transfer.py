"""
字幕翻译模块
"""
import asyncio
from typing import List

import pysrt
from googletrans import Translator

from core.utils.common.logger import log


async def translate_batch(translator: Translator, texts: List[str], target_lang: str) -> List[str]:
    """
    异步批量翻译文本
    
    Args:
        translator: 翻译器实例
        texts: 要翻译的文本列表
        target_lang: 目标语言代码
    
    Returns:
        List[str]: 翻译后的文本列表
    """
    try:
        translations = []
        for text in texts:
            # 逐个翻译以避免批量翻译的问题
            trans = await translator.translate(text, dest=target_lang)
            translations.append(trans.text)
        return translations
    except Exception as e:
        log.error(f"翻译文本时出错: {str(e)}")
        # 如果翻译失败，返回原文
        return texts


async def async_translate_srt_file(srt_path: str, target_path: str, target_lang: str = 'zh-cn') -> str:
    """
    异步翻译SRT字幕文件
    
    Args:
        srt_path: 原始字幕文件路径
        target_lang: 目标语言代码，默认为中文(zh-cn)
    
    Returns:
        str: 翻译后的字幕文件路径
        :param target_lang:
        :param srt_path:
        :param target_path:
    """
    try:
        # 加载字幕文件
        subs = pysrt.open(srt_path)

        # 初始化翻译器
        translator = Translator()

        # 批量翻译，每次处理多个字幕以提高效率
        batch_size = 10  # 减小批次大小以提高稳定性
        total_subs = len(subs)

        for i in range(0, total_subs, batch_size):
            batch = subs[i:min(i + batch_size, total_subs)]
            texts = [sub.text for sub in batch]

            try:
                # 批量翻译
                translations = await translate_batch(translator, texts, target_lang)

                # 更新字幕文本
                for sub, trans in zip(batch, translations):
                    sub.text = trans

            except Exception as e:
                log.error(f"翻译批次 {i}-{i + batch_size} 时出错: {str(e)}")
                # 继续处理下一批
                continue

        # 保存翻译后的字幕文件
        subs.save(target_path, encoding='utf-8')

        return target_path

    except Exception as e:
        log.error(f"翻译字幕文件时出错: {str(e)}")
        raise


def translate_srt_file(srt_path: str, target_path: str, target_lang: str = 'zh-cn') -> str:
    """
    同步包装函数，用于调用异步翻译函数
    
    Args:
        srt_path: 原始字幕文件路径
        target_lang: 目标语言代码，默认为中文(zh-cn)
    
    Returns:
        str: 翻译后的字幕文件路径
    """
    return asyncio.run(async_translate_srt_file(srt_path, target_lang))
