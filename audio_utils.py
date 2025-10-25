#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频处理工具 - 用于前端上传的音频转换
"""

import base64
import io
from pydub import AudioSegment


def convert_webm_to_wav(webm_data: bytes) -> bytes:
    """
    将WebM格式音频转换为WAV格式
    
    参数:
        webm_data: WebM格式的音频数据
    
    返回:
        WAV格式的音频数据
    """
    try:
        # 使用pydub转换格式
        audio = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
        
        # 转换为16k采样率，单声道
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # 导出为WAV
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        
        return wav_io.read()
    except ImportError:
        # 如果没有安装pydub，返回原始数据
        print("⚠️  未安装pydub，无法转换音频格式")
        return webm_data
    except Exception as e:
        print(f"⚠️  音频转换失败: {e}")
        return webm_data


def base64_to_audio(base64_str: str) -> bytes:
    """
    将base64字符串转换为音频数据
    
    参数:
        base64_str: base64编码的音频数据
    
    返回:
        音频二进制数据
    """
    # 移除data URL前缀
    if ',' in base64_str:
        base64_str = base64_str.split(',')[1]
    
    return base64.b64decode(base64_str)

