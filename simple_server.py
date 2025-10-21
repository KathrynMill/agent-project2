#!/usr/bin/env python3
"""
简化的WebSocket服务器 - 用于前端连接测试
"""

import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
from simple_test import SimpleLocalLLM

class SimpleServer:
    def __init__(self):
        self.llm = SimpleLocalLLM()
        self.clients = set()
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """注册客户端"""
        self.clients.add(websocket)
        print(f"客户端已连接: {websocket.remote_address}")
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """注销客户端"""
        self.clients.discard(websocket)
        print(f"客户端已断开: {websocket.remote_address}")
    
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            print(f"收到消息: {data}")
            
            if data.get('type') == 'text':
                # 处理文本消息
                text = data.get('text', '')
                response = await self.llm.generate_response(text)
                intent = await self.llm.parse_intent(text)
                
                # 发送响应
                response_data = {
                    'type': 'response',
                    'message': response['text'],
                    'success': True,
                    'data': {
                        'intent': intent,
                        'confidence': response['confidence']
                    }
                }
                
                await websocket.send(json.dumps(response_data))
                print(f"发送响应: {response_data}")
                
            elif data.get('type') == 'audio':
                # 处理音频消息（简化处理）
                response_data = {
                    'type': 'response',
                    'message': '收到音频消息，正在处理...',
                    'success': True,
                    'data': {
                        'intent': {'intent': 'audio_processing', 'confidence': 0.8}
                    }
                }
                
                await websocket.send(json.dumps(response_data))
                print("处理音频消息")
                
        except Exception as e:
            print(f"处理消息错误: {e}")
            error_response = {
                'type': 'error',
                'error_message': str(e)
            }
            await websocket.send(json.dumps(error_response))
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """处理客户端连接"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self, host='127.0.0.1', port=8000):
        """启动服务器"""
        print(f"🚀 启动WebSocket服务器: ws://{host}:{port}")
        print("=" * 50)
        
        async with websockets.serve(self.handle_client, host, port):
            print("✅ 服务器已启动，等待连接...")
            print("💡 前端地址: http://localhost:5173")
            print("🔗 WebSocket地址: ws://127.0.0.1:8000/ws")
            print("=" * 50)
            
            # 保持服务器运行
            await asyncio.Future()  # 永远等待

async def main():
    server = SimpleServer()
    await server.start_server()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
