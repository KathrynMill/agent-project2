#!/usr/bin/env python3
"""
简化的HTTP服务器 - 用于前端连接测试
"""

import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from simple_test import SimpleLocalLLM
from system_controller import SystemController
from voice_recognition import VoiceRecognition
import threading
import time

class SimpleHTTPHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.llm = SimpleLocalLLM()
        self.system_controller = SystemController()
        self.voice_recognition = VoiceRecognition()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'status': 'ok',
                'message': 'Echo Command Server is running',
                'llm_status': self.llm.get_status()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Echo Command Server</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>🎯 Echo Command Server</h1>
                <p>服务器正在运行...</p>
                <p>前端地址: <a href="http://localhost:5173">http://localhost:5173</a></p>
                <p>状态: <span id="status">检查中...</span></p>
                
                <script>
                    fetch('/health')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('status').textContent = '运行正常';
                            document.getElementById('status').style.color = 'green';
                        })
                        .catch(error => {
                            document.getElementById('status').textContent = '连接失败';
                            document.getElementById('status').style.color = 'red';
                        });
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/voice':
            # 处理语音识别请求
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                audio_data = data.get('audio_data', '')
                
                # 解码音频数据
                if audio_data:
                    import base64
                    audio_bytes = base64.b64decode(audio_data)
                    # 语音识别
                    transcription = self.voice_recognition.transcribe_audio(audio_bytes)
                    
                    if transcription['success']:
                        # 使用识别结果进行对话
                        text = transcription['text']
                        import asyncio
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        response = loop.run_until_complete(self.llm.generate_response(text))
                        intent = loop.run_until_complete(self.llm.parse_intent(text))
                        system_result = self._execute_system_action(intent, text)
                        
                        response_data = {
                            'type': 'voice_response',
                            'transcription': transcription,
                            'message': response['text'],
                            'success': True,
                            'data': {
                                'intent': intent,
                                'confidence': response['confidence'],
                                'system_action': system_result
                            }
                        }
                    else:
                        response_data = {
                            'type': 'voice_error',
                            'message': '语音识别失败',
                            'success': False,
                            'error': transcription.get('error', '未知错误')
                        }
                else:
                    response_data = {
                        'type': 'voice_error',
                        'message': '未收到音频数据',
                        'success': False
                    }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    'type': 'voice_error',
                    'error_message': str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
                
        elif self.path == '/api/chat':
            # 处理聊天请求
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                text = data.get('text', '')
                
                # 生成响应
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                response = loop.run_until_complete(self.llm.generate_response(text))
                intent = loop.run_until_complete(self.llm.parse_intent(text))
                
                # 根据意图执行相应的系统控制操作
                system_result = self._execute_system_action(intent, text)
                
                response_data = {
                    'type': 'response',
                    'message': response['text'],
                    'success': True,
                    'data': {
                        'intent': intent,
                        'confidence': response['confidence'],
                        'system_action': system_result
                    }
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                self.wfile.write(json.dumps(response_data).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                error_response = {
                    'type': 'error',
                    'error_message': str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
                
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _execute_system_action(self, intent, text):
        """根据意图执行系统控制操作"""
        try:
            intent_name = intent.get('intent', '')
            action = intent.get('action', '')
            
            print(f"🎯 执行系统动作: {intent_name} -> {action}")
            
            if intent_name == 'play_music' or action == 'play_music':
                return self.system_controller.play_music(text)
            
            elif intent_name == 'open_browser' or action == 'open_browser':
                return self.system_controller.open_browser()
            
            elif intent_name == 'adjust_volume' or action == 'adjust_volume':
                # 尝试从文本中提取音量级别
                import re
                volume_match = re.search(r'(\d+)', text)
                volume_level = int(volume_match.group(1)) if volume_match else 50
                return self.system_controller.adjust_volume(volume_level)
            
            elif intent_name == 'write_article' or action == 'write_article':
                # 提取文章主题
                topic = text.replace('写', '').replace('文章', '').replace('关于', '').strip()
                if not topic:
                    topic = "AI技术发展"
                return self.system_controller.write_article(topic)
            
            elif intent_name == 'write_code' or action == 'write_code':
                # 写代码功能
                return self.system_controller.write_article("代码示例", f"根据您的需求：{text}，这里是一个代码示例...")
            
            elif intent_name == 'greeting' or action == 'greet':
                # 问候语 - 获取系统信息
                return self.system_controller.get_system_info()
            
            else:
                return {
                    "success": True,
                    "message": "已理解您的需求，但未找到对应的系统操作",
                    "action": "unknown",
                    "intent": intent_name
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"执行系统操作失败: {str(e)}",
                "action": "error",
                "error": str(e)
            }
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def start_server(port=8001):
    """启动HTTP服务器"""
    print(f"🚀 启动HTTP服务器: http://127.0.0.1:{port}")
    print("=" * 50)
    
    with socketserver.TCPServer(("", port), SimpleHTTPHandler) as httpd:
        print("✅ 服务器已启动")
        print(f"💡 健康检查: http://127.0.0.1:{port}/health")
        print(f"💡 前端地址: http://localhost:5173")
        print(f"💡 API端点: http://127.0.0.1:{port}/api/chat")
        print("=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")

if __name__ == "__main__":
    start_server()
