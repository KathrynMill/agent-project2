#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七牛云AI API客户端
支持：语音识别(ASR)、语音合成(TTS)、大模型对话
"""

import requests
import json
import base64
from typing import Dict, Any, List


class QiniuAPIClient:
    """七牛云AI API客户端"""
    
    def __init__(self, api_key: str):
        """
        初始化七牛云API客户端
        
        参数:
            api_key: 七牛云 AI API KEY
        """
        self.api_key = api_key
        self.base_url = "https://openai.qiniu.com/v1"
        self.backup_url = "https://api.qnaigc.com/v1"
        
        print(f"✅ 已配置七牛云API")
        print(f"🔑 API Key: {api_key[:20]}...")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, message: str, history: List[Dict] = None, model: str = "deepseek-v3") -> Dict[str, Any]:
        """
        调用大模型进行对话（使用OpenAI兼容接口）
        
        参数:
            message: 用户消息
            history: 对话历史
            model: 模型名称，默认 deepseek-v3
        
        返回:
            {
                "success": True/False,
                "content": "AI回复内容",
                "error": "错误信息(如果有)"
            }
        """
        url = f"{self.base_url}/chat/completions"
        
        # 构建消息列表
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "content": content,
                    "usage": result.get("usage", {})
                }
            elif "error" in result:
                return {
                    "success": False,
                    "error": result["error"].get("message", "未知错误")
                }
            else:
                return {
                    "success": False,
                    "error": f"API返回格式异常: {result}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"API调用异常: {str(e)}"
            }
    
    def speech_recognition(self, audio_url: str, audio_format: str = "mp3") -> Dict[str, Any]:
        """
        语音识别(ASR) - 将语音转为文字
        
        参数:
            audio_url: 音频文件的公网URL
            audio_format: 音频格式 (mp3/wav/ogg等)
        
        返回:
            {
                "success": True/False,
                "text": "识别出的文字",
                "error": "错误信息(如果有)"
            }
        """
        url = f"{self.base_url}/voice/asr"
        
        payload = {
            "model": "asr",
            "audio": {
                "format": audio_format,
                "url": audio_url
            }
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            result = response.json()
            
            if "data" in result and "result" in result["data"]:
                text = result["data"]["result"].get("text", "")
                return {
                    "success": True,
                    "text": text,
                    "reqid": result.get("reqid", "")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "识别失败")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"语音识别异常: {str(e)}"
            }
    
    def text_to_speech(self, text: str, voice_type: str = "qiniu_zh_female_tmjxxy", 
                      encoding: str = "mp3", speed_ratio: float = 1.0) -> Dict[str, Any]:
        """
        语音合成(TTS) - 将文字转为语音
        
        参数:
            text: 要合成的文字
            voice_type: 音色类型
            encoding: 音频编码格式
            speed_ratio: 语速比例
        
        返回:
            {
                "success": True/False,
                "audio_data": base64编码的音频数据,
                "duration": 音频时长(毫秒),
                "error": "错误信息(如果有)"
            }
        """
        url = f"{self.base_url}/voice/tts"
        
        payload = {
            "audio": {
                "voice_type": voice_type,
                "encoding": encoding,
                "speed_ratio": speed_ratio
            },
            "request": {
                "text": text
            }
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload, timeout=30)
            result = response.json()
            
            if "data" in result:
                # data字段是base64编码的音频数据
                audio_base64 = result["data"]
                duration = result.get("addition", {}).get("duration", "0")
                
                return {
                    "success": True,
                    "audio_data": audio_base64,  # 已经是base64格式
                    "duration": duration,
                    "reqid": result.get("reqid", "")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "合成失败")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"语音合成异常: {str(e)}"
            }
    
    def get_voice_list(self) -> Dict[str, Any]:
        """
        获取可用的音色列表
        
        返回:
            {
                "success": True/False,
                "voices": [音色列表],
                "error": "错误信息(如果有)"
            }
        """
        url = f"{self.base_url}/voice/list"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            voices = response.json()
            
            if isinstance(voices, list):
                return {
                    "success": True,
                    "voices": voices
                }
            else:
                return {
                    "success": False,
                    "error": "获取音色列表失败"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"获取音色列表异常: {str(e)}"
            }


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("七牛云API客户端测试")
    print("=" * 60)
    
    # 使用您提供的API Key
    api_key = "sk-ca1afda060bc12b11cdbc0e7d34a4e1f741325f6685430ceef06f4596eaf90aa"
    client = QiniuAPIClient(api_key=api_key)
    
    # 测试1: 对话功能
    print("\n【测试1: 大模型对话】")
    result = client.chat('请用JSON格式回复。用户说：帮我打开GitHub。请分析意图并返回{"action":"动作","parameters":{参数}}')
    
    if result.get("success"):
        print(f"✅ AI回复: {result.get('content')}")
    else:
        print(f"❌ 错误: {result.get('error')}")
    
    # 测试2: 获取音色列表
    print("\n【测试2: 获取音色列表】")
    result = client.get_voice_list()
    
    if result.get("success"):
        voices = result.get("voices", [])
        print(f"✅ 共有 {len(voices)} 种音色")
        if len(voices) > 0:
            print(f"示例音色: {voices[0].get('voice_name')} ({voices[0].get('voice_type')})")
    else:
        print(f"❌ 错误: {result.get('error')}")
    
    # 测试3: 语音合成
    print("\n【测试3: 语音合成】")
    result = client.text_to_speech("你好，我是智能语音助手")
    
    if result.get("success"):
        print(f"✅ 语音合成成功，时长: {result.get('duration')}毫秒")
    else:
        print(f"❌ 错误: {result.get('error')}")

