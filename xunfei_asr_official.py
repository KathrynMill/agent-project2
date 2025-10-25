#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
讯飞语音识别 - 基于官方Demo改写
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
from typing import Dict, Any

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class XunfeiASROfficial:
    """讯飞语音识别 - 官方Demo版本"""
    
    def __init__(self, appid: str, api_key: str, api_secret: str):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        
        self.result_text = ""
        self.ws = None
        self.audio_data = None
        
        print(f"✅ 讯飞ASR已配置（官方版）")
        print(f"📱 APPID: {appid}")
    
    def create_url(self):
        """生成WebSocket URL"""
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        
        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url
    
    def on_message(self, ws, message):
        """收到websocket消息的处理"""
        try:
            data = json.loads(message)
            code = data.get("code", 0)
            sid = data.get("sid", "")
            
            if code != 0:
                errMsg = data.get("message", "")
                print(f"❌ 识别错误: sid={sid}, code={code}, msg={errMsg}")
                self.result_text = ""
            else:
                # 解析识别结果
                ws_data = data.get("data", {}).get("result", {}).get("ws", [])
                result = ""
                for i in ws_data:
                    for w in i.get("cw", []):
                        result += w.get("w", "")
                
                self.result_text += result
                if result:
                    print(f"📝 识别片段: {result}")
                
        except Exception as e:
            print(f"❌ 消息处理异常: {e}")
    
    def on_error(self, ws, error):
        """收到websocket错误的处理"""
        print(f"❌ WebSocket错误: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """收到websocket关闭的处理"""
        print("🔌 WebSocket连接已关闭")
    
    def on_open(self, ws):
        """收到websocket连接建立的处理"""
        def run(*args):
            try:
                frameSize = 8000  # 每一帧的音频大小
                intervel = 0.04  # 发送音频间隔(单位:s)
                status = STATUS_FIRST_FRAME
                
                audio_data = self.audio_data
                
                # 如果是WAV格式，跳过头部
                if len(audio_data) > 44 and audio_data[:4] == b'RIFF':
                    print("📝 检测到WAV格式，跳过头部44字节")
                    audio_data = audio_data[44:]
                
                print(f"📤 开始发送音频数据，总大小: {len(audio_data)} bytes")
                
                # 分帧发送
                offset = 0
                while offset < len(audio_data):
                    buf = audio_data[offset:offset + frameSize]
                    offset += frameSize
                    
                    # 判断是否为最后一帧
                    if offset >= len(audio_data):
                        status = STATUS_LAST_FRAME
                    
                    # 构建发送数据
                    if status == STATUS_FIRST_FRAME:
                        # 第一帧，带business参数
                        d = {
                            "common": {"app_id": self.appid},
                            "business": {
                                "domain": "iat",
                                "language": "zh_cn",
                                "accent": "mandarin",
                                "vad_eos": 2000,
                                "dwa": "wpgs"  # 开启动态修正（支持中英混合）
                            },
                            "data": {
                                "status": 0,
                                "format": "audio/L16;rate=16000",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        status = STATUS_CONTINUE_FRAME
                        
                    elif status == STATUS_CONTINUE_FRAME:
                        # 中间帧
                        d = {
                            "data": {
                                "status": 1,
                                "format": "audio/L16;rate=16000",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        
                    elif status == STATUS_LAST_FRAME:
                        # 最后一帧
                        d = {
                            "data": {
                                "status": 2,
                                "format": "audio/L16;rate=16000",
                                "audio": base64.b64encode(buf).decode('utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(d))
                        break
                    
                    # 模拟音频采样间隔
                    time.sleep(intervel)
                
                print("✅ 音频数据发送完成")
                time.sleep(1)
                ws.close()
                
            except Exception as e:
                print(f"❌ 发送音频失败: {e}")
                ws.close()
        
        thread.start_new_thread(run, ())
    
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
            websocket.enableTrace(False)
            wsUrl = self.create_url()
            
            print("📡 正在连接讯飞WebSocket...")
            
            self.ws = websocket.WebSocketApp(
                wsUrl,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.on_open = self.on_open
            self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            if self.result_text:
                print(f"✅ 最终识别结果: {self.result_text}")
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
            print(f"❌ 识别失败: {e}")
            return {
                "success": False,
                "error": f"识别失败: {str(e)}"
            }


if __name__ == "__main__":
    print("=" * 60)
    print("讯飞ASR测试（官方版）")
    print("=" * 60)
    
    # 您的密钥
    appid = "dbf06899"
    api_key = "de40e555f7e61b459017c512d863657b"
    api_secret = "OWQyOTY5OWI4OTU0YzYwMDAzYmE1ZGQ4"
    
    client = XunfeiASROfficial(appid, api_key, api_secret)
    print("✅ 配置完成！")

