#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
讯飞WebSocket语音识别 - 更可靠的实时识别方案
"""

import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from typing import Dict, Any
import time


class XunfeiWebSocketASR:
    """讯飞WebSocket语音识别"""
    
    def __init__(self, appid: str, api_key: str, api_secret: str):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.ws_url = "wss://iat-api.xfyun.cn/v2/iat"
        
        self.result_text = ""
        self.ws = None
        self.audio_data = None
        
        print(f"✅ 讯飞WebSocket ASR已配置")
    
    def create_url(self):
        """生成WebSocket鉴权URL"""
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
            data = json.loads(message)
            code = data.get("code", 0)
            
            if code != 0:
                print(f"❌ 识别错误: code={code}, message={data.get('message', '')}")
                self.result_text = ""
                ws.close()
                return
            
            # 解析识别结果
            result_data = data.get("data", {})
            status = result_data.get("status", 0)
            result_list = result_data.get("result", {}).get("ws", [])
            
            # 拼接识别结果
            for item in result_list:
                for word in item.get("cw", []):
                    self.result_text += word.get("w", "")
            
            print(f"📝 识别中: {self.result_text}")
            
            # status=2表示识别结束
            if status == 2:
                print(f"✅ 识别完成: {self.result_text}")
                ws.close()
                
        except Exception as e:
            print(f"❌ 消息处理错误: {e}")
    
    def on_error(self, ws, error):
        """发生错误的回调"""
        print(f"❌ WebSocket错误: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """连接关闭的回调"""
        print("🔌 WebSocket连接已关闭")
    
    def on_open(self, ws):
        """连接建立的回调，发送音频数据"""
        def send_audio():
            try:
                # 发送音频数据
                chunk_size = 1280  # 每次发送1280字节（40ms音频）
                audio_data = self.audio_data
                
                # 如果是WAV格式，跳过头部
                if len(audio_data) > 44 and audio_data[:4] == b'RIFF':
                    print("📝 检测到WAV格式，跳过头部")
                    audio_data = audio_data[44:]
                
                status = 0  # 0:首帧 1:中间帧 2:尾帧
                
                for i in range(0, len(audio_data), chunk_size):
                    chunk = audio_data[i:i + chunk_size]
                    
                    # 判断是否为最后一帧
                    if i + chunk_size >= len(audio_data):
                        status = 2
                    elif i == 0:
                        status = 0
                    else:
                        status = 1
                    
                    # 构建发送数据
                    frame = {
                        "common": {
                            "app_id": self.appid
                        },
                        "business": {
                            "language": "zh_cn",
                            "domain": "iat",
                            "accent": "mandarin",
                            "vad_eos": 2000,
                            "dwa": "wpgs"
                        },
                        "data": {
                            "status": status,
                            "format": "audio/L16;rate=16000",
                            "encoding": "raw",
                            "audio": base64.b64encode(chunk).decode()
                        }
                    }
                    
                    # 只在首帧发送business参数
                    if status != 0:
                        del frame["business"]
                    
                    ws.send(json.dumps(frame))
                    time.sleep(0.04)  # 模拟40ms间隔
                
                print("📤 音频数据发送完成")
                
            except Exception as e:
                print(f"❌ 发送音频失败: {e}")
                ws.close()
        
        # 在新线程中发送音频
        import threading
        threading.Thread(target=send_audio).start()
    
    def recognize(self, audio_data: bytes) -> Dict[str, Any]:
        """
        识别音频
        
        参数:
            audio_data: 音频二进制数据（PCM/WAV格式，16kHz，16bit，单声道）
        
        返回:
            识别结果
        """
        self.result_text = ""
        self.audio_data = audio_data
        
        try:
            # 创建WebSocket连接
            websocket.enableTrace(False)
            ws_url = self.create_url()
            
            self.ws = websocket.WebSocketApp(
                ws_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )
            
            print("📡 正在连接讯飞WebSocket...")
            
            # 运行WebSocket（会阻塞直到连接关闭）
            self.ws.run_forever(
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )
            
            if self.result_text:
                return {
                    "success": True,
                    "text": self.result_text
                }
            else:
                return {
                    "success": False,
                    "error": "识别结果为空"
                }
                
        except Exception as e:
            print(f"❌ WebSocket识别失败: {e}")
            return {
                "success": False,
                "error": f"WebSocket识别失败: {str(e)}"
            }


if __name__ == "__main__":
    print("讯飞WebSocket ASR测试")
    print("=" * 60)
    
    # 测试配置
    appid = "dbf06899"
    api_key = "de40e555f7e61b459017c512d863657b"
    api_secret = "OWQyOTY5OWI4OTU0YzYwMDAzYmE1ZGQ4"
    
    client = XunfeiWebSocketASR(appid, api_key, api_secret)
    print("✅ 配置成功！")

