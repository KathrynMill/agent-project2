#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讯飞语音识别客户端（WebSocket实时识别）
文档：https://www.xfyun.cn/doc/asr/voicedictation/API.html
"""

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread


class XunfeiASRClient:
    """讯飞语音识别客户端"""
    
    def __init__(self, appid, api_key, api_secret):
        """
        初始化讯飞ASR客户端
        
        参数:
            appid: 讯飞开放平台的APPID
            api_key: API Key
            api_secret: API Secret
        
        获取方式：
        1. 注册讯飞开放平台账号：https://www.xfyun.cn/
        2. 创建应用：https://console.xfyun.cn/app/myapp
        3. 获取APPID、API Key、API Secret
        """
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        
        self.ws_url = "wss://iat-api.xfyun.cn/v2/iat"
        self.result_text = ""
        self.ws = None
        
    def create_url(self):
        """生成鉴权URL"""
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 拼接字符串
        signature_origin = f"host: iat-api.xfyun.cn\n"
        signature_origin += f"date: {date}\n"
        signature_origin += f"GET /v2/iat HTTP/1.1"
        
        # 进行hmac-sha256加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat-api.xfyun.cn"
        }
        
        # 拼接鉴权参数，生成URL
        url = self.ws_url + '?' + urlencode(v)
        return url
    
    def on_message(self, ws, message):
        """收到消息的回调"""
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            
            if code != 0:
                errMsg = json.loads(message)["message"]
                print(f"❌ 识别失败: {errMsg}")
                ws.close()
            else:
                data = json.loads(message)["data"]["result"]["ws"]
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                
                self.result_text += result
                print(f"识别结果: {result}")
                
                # 判断是否为最后一帧
                if json.loads(message)["data"]["status"] == 2:
                    print(f"✅ 最终识别结果: {self.result_text}")
                    ws.close()
        except Exception as e:
            print(f"消息处理错误: {e}")
    
    def on_error(self, ws, error):
        """发生错误的回调"""
        print(f"❌ WebSocket错误: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭的回调"""
        print("🔌 WebSocket连接已关闭")
    
    def on_open(self, ws):
        """连接建立的回调"""
        def run(*args):
            # 这里应该读取音频文件并发送
            # 音频格式要求：PCM, 16k采样率, 16bit, 单声道
            print("📡 WebSocket连接已建立")
            
            # 发送音频数据的代码在这里
            # 由于需要实际的音频流，这里只是示例框架
            
        thread.start_new_thread(run, ())
    
    def recognize_audio_file(self, audio_file_path):
        """
        识别音频文件
        
        参数:
            audio_file_path: 音频文件路径（PCM格式，16k采样率）
        
        返回:
            识别出的文字
        """
        self.result_text = ""
        
        # 创建WebSocket连接
        websocket.enableTrace(False)
        ws_url = self.create_url()
        
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        return self.result_text


# 简化版本：使用讯飞的HTTP API（更简单）
class XunfeiASRSimple:
    """讯飞语音识别 - HTTP API版本（更简单）"""
    
    def __init__(self, appid, api_key):
        """
        初始化
        
        参数:
            appid: 讯飞APPID
            api_key: API Key
        """
        self.appid = appid
        self.api_key = api_key
        self.api_url = "https://api.xfyun.cn/v1/service/v1/iat"
    
    def recognize(self, audio_data, audio_format="wav", sample_rate=16000):
        """
        语音识别
        
        参数:
            audio_data: 音频二进制数据
            audio_format: 音频格式（wav/pcm）
            sample_rate: 采样率
        
        返回:
            识别结果
        """
        # 注意：这需要根据讯飞实际的HTTP API文档来实现
        # 这里只是示例框架
        
        import requests
        
        # 构建请求参数（需要根据实际文档调整）
        params = {
            "engine_type": "sms16k",
            "aue": "raw"
        }
        
        headers = {
            "X-Appid": self.appid,
            "X-CurTime": str(int(time.time())),
            "X-Param": base64.b64encode(json.dumps(params).encode()).decode(),
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=audio_data,
                timeout=10
            )
            
            result = response.json()
            return result
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("讯飞语音识别客户端")
    print("=" * 60)
    print("\n📌 使用步骤：")
    print("1. 访问 https://www.xfyun.cn/ 注册账号")
    print("2. 创建应用获取 APPID、API Key、API Secret")
    print("3. 配置到代码中即可使用")
    print("\n💡 优势：")
    print("✅ 国内服务，不被墙")
    print("✅ 免费额度：每天500次")
    print("✅ 精度高，支持实时识别")
    print("✅ WebSocket方式，适合语音对话")

