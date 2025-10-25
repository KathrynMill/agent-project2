#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音助手服务器 - 主服务
整合：百度API、智能Agent、系统控制器
"""

import http.server
import socketserver
import json
import os
import base64
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

from baidu_api_client import BaiduAPIClient, BaiduAPIDemoClient
from qiniu_api_client import QiniuAPIClient
from xunfei_client import XunfeiClient
from intelligent_agent import IntelligentAgent
from system_controller import SystemController


class VoiceAssistantHandler(http.server.SimpleHTTPRequestHandler):
    """语音助手HTTP请求处理器"""
    
    # 类级别的共享实例
    api_client = None
    xunfei_client = None
    agent = None
    controller = None
    
    @classmethod
    def initialize_components(cls):
        """初始化组件（只初始化一次）"""
        if cls.api_client is None:
            print("🚀 初始化语音助手组件...")
            
            # 使用七牛云LLM
            qiniu_api_key = "sk-ca1afda060bc12b11cdbc0e7d34a4e1f741325f6685430ceef06f4596eaf90aa"
            cls.api_client = QiniuAPIClient(api_key=qiniu_api_key)
            
            # 使用讯飞语音识别
            cls.xunfei_client = XunfeiClient(
                appid="dbf06899",
                api_key="de40e555f7e61b459017c512d863657b",
                api_secret="OWQyOTY5OWI4OTU0YzYwMDAzYmE1ZGQ4"
            )
            
            # 初始化智能Agent
            cls.agent = IntelligentAgent(cls.api_client)
            
            # 初始化系统控制器
            cls.controller = SystemController()
            
            print("✅ 组件初始化完成")
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        
        # 健康检查
        if parsed_path.path == '/health':
            self.send_json_response({"status": "ok", "message": "服务运行中"})
            return
        
        # API信息
        if parsed_path.path == '/api/info':
            self.send_json_response({
                "name": "智能语音助手",
                "version": "1.0.0",
                "features": ["语音识别", "语音合成", "智能对话", "系统控制"],
                "demo_mode": isinstance(self.api_client, BaiduAPIDemoClient)
            })
            return
        
        # 对话历史
        if parsed_path.path == '/api/history':
            history = self.agent.get_conversation_history()
            self.send_json_response({"success": True, "history": history})
            return
        
        # 静态文件服务
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            self.path = '/frontend/index.html'
        
        return super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        request_body = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(request_body.decode('utf-8'))
        except Exception as e:
            self.send_json_response({
                "success": False,
                "error": f"JSON解析失败: {str(e)}"
            }, status_code=400)
            return
        
        # 路由到不同的处理方法
        if parsed_path.path == '/api/text':
            self.handle_text_input(request_data)
        
        elif parsed_path.path == '/api/voice':
            self.handle_voice_input(request_data)
        
        elif parsed_path.path == '/api/tts':
            self.handle_tts(request_data)
        
        elif parsed_path.path == '/api/chat':
            self.handle_chat(request_data)
        
        else:
            self.send_json_response({
                "success": False,
                "error": f"未知的API端点: {parsed_path.path}"
            }, status_code=404)
    
    def handle_text_input(self, request_data: Dict[str, Any]):
        """
        处理文本输入
        
        请求格式:
        {
            "text": "用户输入的文本"
        }
        """
        text = request_data.get('text', '').strip()
        
        if not text:
            self.send_json_response({
                "success": False,
                "error": "文本不能为空"
            }, status_code=400)
            return
        
        print(f"\n{'='*60}")
        print(f"📥 收到文本输入: {text}")
        print(f"{'='*60}")
        
        # 使用Agent处理用户输入
        agent_result = self.agent.process_user_input(text)
        
        # 如果Agent返回了工具调用，执行系统操作
        if agent_result.get('success'):
            action = agent_result.get('action') or agent_result.get('tool')
            # 优先使用agent_result中的参数，fallback到parameters字段
            parameters = dict(agent_result.get('parameters', {}))
            # 如果parameters为空，尝试从agent_result的其他字段获取
            if not parameters:
                for key in ['url', 'target_name', 'song_name', 'artist', 'topic', 'query']:
                    if key in agent_result:
                        parameters[key] = agent_result[key]
            
            # 执行系统操作
            execution_result = self.controller.execute_action(action, parameters)
            
            # 合并结果
            response = {
                "success": True,
                "text": text,
                "intent": {
                    "action": action,
                    "parameters": parameters
                },
                "execution": execution_result,
                "message": execution_result.get('message', ''),
                "tts_text": execution_result.get('message', '')
            }
        else:
            response = {
                "success": agent_result.get('success', False),
                "text": text,
                "message": agent_result.get('message', ''),
                "error": agent_result.get('error'),
                "tts_text": agent_result.get('message', '')
            }
        
        self.send_json_response(response)
    
    def handle_voice_input(self, request_data: Dict[str, Any]):
        """
        处理语音输入
        
        请求格式:
        {
            "audio_data": "base64编码的音频数据",
            "format": "音频格式(pcm/wav)",
            "rate": 16000
        }
        或者直接发文本（用于测试）:
        {
            "audio_data": "测试文本"
        }
        """
        audio_data = request_data.get('audio_data', '')
        audio_format = request_data.get('format', 'pcm')
        sample_rate = request_data.get('rate', 16000)
        
        if not audio_data:
            self.send_json_response({
                "success": False,
                "error": "音频数据不能为空"
            }, status_code=400)
            return
        
        print(f"\n{'='*60}")
        print(f"🎤 收到语音输入")
        print(f"{'='*60}")
        
        # 判断是真实音频还是文本（用于测试）
        if isinstance(audio_data, str) and not audio_data.startswith('data:'):
            # 直接是文本，跳过ASR
            recognized_text = audio_data
            asr_success = True
        else:
            # 真实音频，使用讯飞语音识别
            try:
                # 如果是base64编码，解码
                if audio_data.startswith('data:'):
                    audio_data = audio_data.split(',')[1]
                
                audio_bytes = base64.b64decode(audio_data)
                
                print(f"📤 使用讯飞ASR识别，音频大小: {len(audio_bytes)} bytes")
                
                # 调用讯飞语音识别
                asr_result = self.xunfei_client.speech_recognition(
                    audio_bytes, 
                    format=audio_format, 
                    rate=sample_rate
                )
                
                if not asr_result.get('success'):
                    self.send_json_response({
                        "success": False,
                        "error": f"讯飞语音识别失败: {asr_result.get('error')}"
                    })
                    return
                
                recognized_text = asr_result.get('text', '')
                asr_success = True
                print(f"✅ 讯飞识别成功: {recognized_text}")
                
            except Exception as e:
                self.send_json_response({
                    "success": False,
                    "error": f"音频处理失败: {str(e)}"
                })
                return
        
        print(f"📝 识别结果: {recognized_text}")
        
        # 使用Agent处理识别出的文本
        agent_result = self.agent.process_user_input(recognized_text)
        
        # 执行系统操作
        if agent_result.get('success'):
            action = agent_result.get('action') or agent_result.get('tool')
            # 优先使用agent_result中的参数，fallback到parameters字段
            parameters = dict(agent_result.get('parameters', {}))
            # 如果parameters为空，尝试从agent_result的其他字段获取
            if not parameters:
                for key in ['url', 'target_name', 'song_name', 'artist', 'topic', 'query']:
                    if key in agent_result:
                        parameters[key] = agent_result[key]
            
            execution_result = self.controller.execute_action(action, parameters)
            
            response = {
                "success": True,
                "recognized_text": recognized_text,
                "intent": {
                    "action": action,
                    "parameters": parameters
                },
                "execution": execution_result,
                "message": execution_result.get('message', ''),
                "tts_text": execution_result.get('message', '')
            }
        else:
            response = {
                "success": agent_result.get('success', False),
                "recognized_text": recognized_text,
                "message": agent_result.get('message', ''),
                "error": agent_result.get('error'),
                "tts_text": agent_result.get('message', '')
            }
        
        self.send_json_response(response)
    
    def handle_tts(self, request_data: Dict[str, Any]):
        """
        处理TTS请求
        
        请求格式:
        {
            "text": "要合成的文本"
        }
        """
        text = request_data.get('text', '')
        
        if not text:
            self.send_json_response({
                "success": False,
                "error": "文本不能为空"
            }, status_code=400)
            return
        
        # 调用TTS
        tts_result = self.api_client.text_to_speech(text)
        
        if tts_result.get('success'):
            # 将音频数据转为base64
            audio_data = tts_result.get('audio_data', b'')
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            self.send_json_response({
                "success": True,
                "audio_data": audio_base64,
                "text": text
            })
        else:
            self.send_json_response({
                "success": False,
                "error": tts_result.get('error')
            })
    
    def handle_chat(self, request_data: Dict[str, Any]):
        """
        处理纯对话请求（不执行系统操作）
        
        请求格式:
        {
            "message": "用户消息",
            "history": [对话历史]
        }
        """
        message = request_data.get('message', '')
        history = request_data.get('history', [])
        
        if not message:
            self.send_json_response({
                "success": False,
                "error": "消息不能为空"
            }, status_code=400)
            return
        
        # 调用LLM对话
        chat_result = self.api_client.chat(message, history)
        
        self.send_json_response(chat_result)
    
    def send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_json = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    """主函数"""
    HOST = "0.0.0.0"
    PORT = 8090
    
    print("=" * 60)
    print("🎙️  智能语音助手服务器")
    print("=" * 60)
    
    # 初始化组件
    VoiceAssistantHandler.initialize_components()
    
    # 创建服务器（允许端口重用）
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), VoiceAssistantHandler) as httpd:
        print(f"\n✅ 服务器启动成功!")
        print(f"🌐 访问地址: http://localhost:{PORT}")
        print(f"📡 API端点:")
        print(f"   - POST /api/text      文本输入")
        print(f"   - POST /api/voice     语音输入")
        print(f"   - POST /api/tts       语音合成")
        print(f"   - POST /api/chat      纯对话")
        print(f"   - GET  /api/history   对话历史")
        print(f"   - GET  /health        健康检查")
        print(f"\n💡 提示: 首次使用需配置百度API Key")
        print(f"📝 配置方法: 编辑 baidu_api_client.py 中的 API_KEY 和 SECRET_KEY")
        print(f"\n按 Ctrl+C 停止服务器")
        print("=" * 60 + "\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 服务器已停止")


if __name__ == "__main__":
    main()

