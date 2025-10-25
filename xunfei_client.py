#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讯飞语音识别 - 实用版本
使用HTTP API，简单易用
"""

import requests
import json
import base64
import hashlib
import hmac
import time
from datetime import datetime
from typing import Dict, Any
from xunfei_asr_official import XunfeiASROfficial


class XunfeiClient:
    """讯飞API客户端 - 语音识别和语音合成"""
    
    def __init__(self, appid: str, api_key: str, api_secret: str):
        """
        初始化讯飞客户端
        
        参数:
            appid: 讯飞APPID
            api_key: API Key  
            api_secret: API Secret
        """
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        
        # 初始化WebSocket ASR客户端（官方版）
        self.websocket_asr = XunfeiASROfficial(appid, api_key, api_secret)
        
        print(f"✅ 讯飞API已配置")
        print(f"📱 APPID: {appid}")
    
    def speech_recognition(self, audio_data: bytes, format: str = "wav", rate: int = 16000) -> Dict[str, Any]:
        """
        语音识别 - 使用WebSocket API（更可靠）
        
        参数:
            audio_data: 音频二进制数据
            format: 音频格式 (wav/pcm)
            rate: 采样率
        
        返回:
            识别结果
        """
        print(f"📤 使用讯飞WebSocket ASR")
        print(f"📊 音频数据大小: {len(audio_data)} bytes")
        
        try:
            # 使用WebSocket方式识别
            result = self.websocket_asr.recognize(audio_data)
            return result
        except Exception as e:
            print(f"❌ WebSocket识别失败: {e}")
            return {
                "success": False,
                "error": f"WebSocket识别失败: {str(e)}"
            }
    
    def text_to_speech(self, text: str) -> Dict[str, Any]:
        """
        语音合成
        
        参数:
            text: 要合成的文字
        
        返回:
            合成的音频数据
        """
        url = "https://api.xfyun.cn/v1/service/v1/tts"
        
        param = {
            "auf": "audio/L16;rate=16000",
            "aue": "lame",  # mp3格式
            "voice_name": "xiaoyan",  # 发音人
            "speed": "50",  # 语速
            "volume": "50",  # 音量
            "pitch": "50",  # 音调
            "engine_type": "aisound"
        }
        
        # 生成签名
        cur_time = str(int(time.time()))
        param_base64 = base64.b64encode(json.dumps(param).encode()).decode()
        
        checksum_str = self.api_key + cur_time + param_base64 + text
        checksum = hashlib.md5(checksum_str.encode()).hexdigest()
        
        headers = {
            "X-Appid": self.appid,
            "X-CurTime": cur_time,
            "X-Param": param_base64,
            "X-CheckSum": checksum,
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                data=f"text={text}".encode('utf-8'),
                timeout=30
            )
            
            # 检查返回类型
            content_type = response.headers.get('Content-Type', '')
            
            if 'audio' in content_type:
                # 返回音频数据
                return {
                    "success": True,
                    "audio_data": response.content
                }
            else:
                # 返回错误信息
                result = response.json()
                return {
                    "success": False,
                    "error": result.get("desc", "合成失败")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"API调用异常: {str(e)}"
            }
    
    def chat(self, message: str, history: list = None) -> Dict[str, Any]:
        """
        对话功能 - 兼容接口
        这里实际不使用讯飞的对话，而是使用七牛云的LLM
        """
        return {
            "success": False,
            "error": "请使用七牛云LLM进行对话"
        }


if __name__ == "__main__":
    print("=" * 60)
    print("讯飞API客户端测试")
    print("=" * 60)
    
    # 您的讯飞密钥配置
    appid = "dbf06899"
    api_key = "de40e555f7e61b459017c512d863657b"
    api_secret = "OWQyOTY5OWI4OTU0YzYwMDAzYmE1ZGQ4"
    
    if appid == "YOUR_APPID":
        print("\n⚠️  请先配置您的讯飞密钥！")
        print("\n获取步骤：")
        print("1. 访问 https://www.xfyun.cn/")
        print("2. 注册并创建应用")
        print("3. 获取 APPID、API Key、API Secret")
        print("4. 替换上面的配置")
    else:
        client = XunfeiClient(appid, api_key, api_secret)
        print("\n✅ 配置成功！可以使用语音识别和语音合成功能")

