#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用LLM客户端 - 支持多种大模型API
"""

import requests
import json
from typing import Dict, Any, List


class OpenAICompatibleClient:
    """
    OpenAI兼容格式的API客户端
    支持：OpenAI、DeepSeek、硅基流动等
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.siliconflow.cn/v1"):
        """
        初始化客户端
        
        参数:
            api_key: API密钥
            base_url: API基础URL（默认使用硅基流动）
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = "deepseek-ai/DeepSeek-V2.5"  # 默认模型
        
        print(f"✅ 已配置真实LLM: {base_url}")
        print(f"📦 使用模型: {self.model}")
    
    def chat(self, message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """
        调用LLM进行对话
        
        参数:
            message: 用户消息
            history: 对话历史
        
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
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
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
    
    def speech_recognition(self, audio_data: bytes, format: str = "pcm", rate: int = 16000) -> Dict[str, Any]:
        """
        语音识别（需要单独的ASR服务）
        这里返回提示信息
        """
        return {
            "success": False,
            "error": "当前LLM服务不支持语音识别，请使用百度或其他ASR服务"
        }
    
    def text_to_speech(self, text: str, output_file: str = None) -> Dict[str, Any]:
        """
        语音合成（需要单独的TTS服务）
        这里返回提示信息
        """
        print(f"💬 AI回复: {text}")
        return {
            "success": True,
            "audio_data": b"",
            "message": "当前LLM服务不支持TTS"
        }


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("LLM客户端测试")
    print("=" * 60)
    
    # 使用您提供的API Key
    api_key = "sk-ca1afda060bc12b11cdbc0e7d34a4e1f741325f6685430ceef06f4596eaf90aa"
    client = OpenAICompatibleClient(api_key=api_key)
    
    # 测试对话
    print("\n【测试: LLM对话】")
    result = client.chat("请用JSON格式回复。用户说：帮我打开GitHub。请分析意图并返回{\"action\":\"动作\",\"parameters\":{参数}}")
    
    if result.get("success"):
        print(f"✅ AI回复: {result.get('content')}")
    else:
        print(f"❌ 错误: {result.get('error')}")

