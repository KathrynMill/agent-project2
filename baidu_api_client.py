#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度AI开放平台API客户端
集成：文心一言(LLM)、语音识别(ASR)、语音合成(TTS)
"""

import requests
import json
import base64
import time
from typing import Dict, Optional, Any


class BaiduAPIClient:
    """百度API统一客户端"""
    
    def __init__(self, api_key: str = "", secret_key: str = ""):
        """
        初始化百度API客户端
        
        参数:
            api_key: 百度API Key
            secret_key: 百度Secret Key
        """
        self.api_key = api_key or "YOUR_API_KEY"
        self.secret_key = secret_key or "YOUR_SECRET_KEY"
        self.access_token = None
        self.token_expire_time = 0
        
    def _get_access_token(self) -> str:
        """
        获取百度API的access_token
        token有效期30天，这里做了缓存
        """
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token
            
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        try:
            response = requests.post(url, params=params, timeout=10)
            result = response.json()
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                # 设置过期时间为29天后（提前1天刷新）
                self.token_expire_time = time.time() + (29 * 24 * 3600)
                return self.access_token
            else:
                print(f"获取access_token失败: {result}")
                return ""
        except Exception as e:
            print(f"获取access_token异常: {e}")
            return ""
    
    def chat(self, message: str, history: list = None) -> Dict[str, Any]:
        """
        调用文心一言API进行对话
        
        参数:
            message: 用户消息
            history: 对话历史 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        
        返回:
            {
                "success": True/False,
                "content": "AI回复内容",
                "error": "错误信息(如果有)"
            }
        """
        token = self._get_access_token()
        if not token:
            return {"success": False, "error": "无法获取access_token"}
        
        # 文心一言API地址
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={token}"
        
        # 构建消息列表
        messages = history or []
        messages.append({"role": "user", "content": message})
        
        payload = {
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.9,
            "penalty_score": 1.0,
            "disable_search": False,
            "enable_citation": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if "result" in result:
                return {
                    "success": True,
                    "content": result["result"],
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error_msg", "未知错误")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"API调用异常: {str(e)}"
            }
    
    def speech_recognition(self, audio_data: bytes, format: str = "pcm", rate: int = 16000) -> Dict[str, Any]:
        """
        语音识别(ASR) - 将语音转为文字
        
        参数:
            audio_data: 音频二进制数据
            format: 音频格式 pcm/wav/amr/m4a
            rate: 采样率 8000/16000
        
        返回:
            {
                "success": True/False,
                "text": "识别出的文字",
                "error": "错误信息(如果有)"
            }
        """
        token = self._get_access_token()
        if not token:
            return {"success": False, "error": "无法获取access_token"}
        
        url = f"https://vop.baidu.com/server_api"
        
        # Base64编码音频数据
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        payload = {
            "format": format,
            "rate": rate,
            "channel": 1,
            "cuid": "python_client",
            "token": token,
            "speech": audio_base64,
            "len": len(audio_data)
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("err_no") == 0:
                return {
                    "success": True,
                    "text": result.get("result", [""])[0]
                }
            else:
                return {
                    "success": False,
                    "error": result.get("err_msg", "识别失败")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"语音识别异常: {str(e)}"
            }
    
    def text_to_speech(self, text: str, output_file: str = None) -> Dict[str, Any]:
        """
        语音合成(TTS) - 将文字转为语音
        
        参数:
            text: 要合成的文字
            output_file: 输出音频文件路径（可选）
        
        返回:
            {
                "success": True/False,
                "audio_data": 音频二进制数据,
                "file_path": 保存的文件路径(如果指定),
                "error": "错误信息(如果有)"
            }
        """
        token = self._get_access_token()
        if not token:
            return {"success": False, "error": "无法获取access_token"}
        
        url = "https://tsn.baidu.com/text2audio"
        
        params = {
            "tok": token,
            "tex": text,
            "per": 0,  # 发音人选择，0为女声，1为男声
            "spd": 5,  # 语速，取值0-15，默认为5
            "pit": 5,  # 音调，取值0-15，默认为5
            "vol": 5,  # 音量，取值0-15，默认为5
            "aue": 3,  # 音频格式，3为mp3格式
            "cuid": "python_client",
            "lan": "zh",
            "ctp": 1
        }
        
        try:
            response = requests.post(url, data=params, timeout=10)
            
            # 检查是否返回的是音频数据
            if response.headers['Content-Type'] == "audio/mp3":
                audio_data = response.content
                
                result = {"success": True, "audio_data": audio_data}
                
                # 如果指定了输出文件，保存音频
                if output_file:
                    with open(output_file, 'wb') as f:
                        f.write(audio_data)
                    result["file_path"] = output_file
                
                return result
            else:
                # 返回的是错误信息（JSON格式）
                error_info = response.json()
                return {
                    "success": False,
                    "error": error_info.get("err_msg", "合成失败")
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"语音合成异常: {str(e)}"
            }


# ============================================================
# 演示模式 - 仅用于测试系统架构
# ⚠️ 注意：这不是真正的LLM，只是规则匹配！
# 要使用真正的大模型，请配置真实的API Key
# ============================================================
class BaiduAPIDemoClient(BaiduAPIClient):
    """
    百度API演示客户端 - 仅用于没有API Key时的测试
    
    ⚠️ 重要：此类使用规则匹配（if-else），不是真正的LLM！
    仅用于演示系统架构和流程，不具备真正的AI理解能力。
    
    要使用真正的大模型智能理解，请：
    1. 获取百度API Key
    2. 使用 BaiduAPIClient(api_key="...", secret_key="...")
    """
    
    def __init__(self):
        super().__init__()
        self.demo_mode = True
        print("⚠️  演示模式：使用规则匹配（不是真正的LLM）")
        print("💡 获取真实LLM能力: https://console.bce.baidu.com/ai/")
    
    def chat(self, message: str, history: list = None) -> Dict[str, Any]:
        """演示模式的对话响应"""
        print(f"📝 用户: {message}")
        
        # 简单的规则响应（仅用于演示）
        response_text = self._generate_demo_response(message)
        
        return {
            "success": True,
            "content": response_text,
            "demo_mode": True
        }
    
    def _generate_demo_response(self, message: str) -> str:
        """生成演示响应"""
        message_lower = message.lower()
        
        # 智能分析用户意图并给出指令
        if "打开" in message or "访问" in message:
            if "github" in message_lower:
                return '{"action": "open_website", "target": "github", "url": "https://github.com"}'
            elif "百度" in message or "baidu" in message_lower:
                return '{"action": "open_website", "target": "百度", "url": "https://www.baidu.com"}'
            elif "谷歌" in message or "google" in message_lower:
                return '{"action": "open_website", "target": "谷歌", "url": "https://www.google.com"}'
            else:
                return '{"action": "open_browser", "message": "正在打开浏览器"}'
        
        elif "播放" in message or "音乐" in message or "歌" in message:
            song = "未指定歌曲"
            if "周杰伦" in message:
                song = "周杰伦的歌曲"
            elif "稻香" in message:
                song = "稻香"
            return f'{{"action": "play_music", "song": "{song}", "message": "正在为您播放音乐"}}'
        
        elif "写" in message or "文章" in message or "创作" in message:
            topic = "人工智能"
            if "关于" in message:
                parts = message.split("关于")
                if len(parts) > 1:
                    topic = parts[1].split("的")[0].strip()
            return f'{{"action": "write_article", "topic": "{topic}", "message": "正在为您创作文章"}}'
        
        elif "代码" in message or "编程" in message:
            return '{"action": "generate_code", "message": "正在为您生成代码"}'
        
        elif "搜索" in message or "查询" in message:
            return '{"action": "web_search", "message": "正在为您搜索"}'
        
        else:
            return f'{{"action": "general_response", "message": "我理解了您的需求：{message}"}}'
    
    def speech_recognition(self, audio_data: bytes, format: str = "pcm", rate: int = 16000) -> Dict[str, Any]:
        """演示模式的语音识别"""
        return {
            "success": True,
            "text": "帮我打开GitHub",
            "demo_mode": True
        }
    
    def text_to_speech(self, text: str, output_file: str = None) -> Dict[str, Any]:
        """演示模式的语音合成"""
        print(f"🔊 TTS: {text}")
        return {
            "success": True,
            "audio_data": b"demo_audio_data",
            "demo_mode": True
        }


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("百度API客户端测试")
    print("=" * 60)
    
    # 使用演示模式
    client = BaiduAPIDemoClient()
    
    # 测试对话
    print("\n【测试1: 对话功能】")
    result = client.chat("帮我打开GitHub网站")
    print(f"AI回复: {result.get('content')}")
    
    print("\n【测试2: 复杂任务】")
    result = client.chat("播放周杰伦的稻香")
    print(f"AI回复: {result.get('content')}")
    
    print("\n【测试3: 内容创作】")
    result = client.chat("写一篇关于人工智能的文章")
    print(f"AI回复: {result.get('content')}")

