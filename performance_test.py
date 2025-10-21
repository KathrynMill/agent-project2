#!/usr/bin/env python3
"""
Echo Command 性能测试脚本
"""
import asyncio
import aiohttp
import time
import json
import statistics
from concurrent.futures import ThreadPoolExecutor
import websockets
import base64
import numpy as np

class PerformanceTester:
    def __init__(self, backend_url="http://localhost:8000", cloud_url="http://localhost:8080/api"):
        self.backend_url = backend_url
        self.cloud_url = cloud_url
        self.results = {}
    
    async def test_backend_health(self):
        """测试后端健康检查性能"""
        print("测试后端健康检查...")
        
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.get(f"{self.backend_url}/health") as response:
                end_time = time.time()
                
                if response.status == 200:
                    response_time = (end_time - start_time) * 1000
                    self.results['backend_health'] = {
                        'status': 'success',
                        'response_time_ms': response_time,
                        'status_code': response.status
                    }
                    print(f"✅ 后端健康检查: {response_time:.2f}ms")
                else:
                    self.results['backend_health'] = {
                        'status': 'failed',
                        'status_code': response.status
                    }
                    print(f"❌ 后端健康检查失败: {response.status}")
    
    async def test_websocket_connection(self, num_connections=10):
        """测试WebSocket连接性能"""
        print(f"测试WebSocket连接 ({num_connections}个连接)...")
        
        async def create_connection(conn_id):
            try:
                uri = f"ws://localhost:8000/ws"
                async with websockets.connect(uri) as websocket:
                    # 发送测试消息
                    message = {
                        "type": "text",
                        "text": f"测试消息 {conn_id}",
                        "session_id": None
                    }
                    
                    start_time = time.time()
                    await websocket.send(json.dumps(message))
                    
                    # 等待响应
                    response = await websocket.recv()
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    return {
                        'connection_id': conn_id,
                        'response_time_ms': response_time,
                        'status': 'success'
                    }
            except Exception as e:
                return {
                    'connection_id': conn_id,
                    'status': 'failed',
                    'error': str(e)
                }
        
        # 并发创建连接
        tasks = [create_connection(i) for i in range(num_connections)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_connections = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
        response_times = [r['response_time_ms'] for r in successful_connections]
        
        if response_times:
            self.results['websocket_connections'] = {
                'total_connections': num_connections,
                'successful_connections': len(successful_connections),
                'success_rate': len(successful_connections) / num_connections,
                'avg_response_time_ms': statistics.mean(response_times),
                'min_response_time_ms': min(response_times),
                'max_response_time_ms': max(response_times),
                'median_response_time_ms': statistics.median(response_times)
            }
            print(f"✅ WebSocket连接测试: {len(successful_connections)}/{num_connections} 成功")
            print(f"   平均响应时间: {statistics.mean(response_times):.2f}ms")
        else:
            self.results['websocket_connections'] = {
                'status': 'failed',
                'error': '所有连接都失败了'
            }
            print("❌ WebSocket连接测试失败")
    
    async def test_text_processing_performance(self, num_requests=50):
        """测试文本处理性能"""
        print(f"测试文本处理性能 ({num_requests}个请求)...")
        
        test_texts = [
            "打开记事本",
            "调节音量到50%",
            "播放音乐",
            "截图",
            "写一篇关于AI的文章",
            "查看系统信息",
            "创建文件",
            "删除文件",
            "搜索文件",
            "翻译文本"
        ]
        
        async def send_text_request(session, text, request_id):
            try:
                uri = f"ws://localhost:8000/ws"
                async with websockets.connect(uri) as websocket:
                    message = {
                        "type": "text",
                        "text": text,
                        "session_id": None
                    }
                    
                    start_time = time.time()
                    await websocket.send(json.dumps(message))
                    
                    # 等待响应
                    response = await websocket.recv()
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    return {
                        'request_id': request_id,
                        'text': text,
                        'response_time_ms': response_time,
                        'status': 'success'
                    }
            except Exception as e:
                return {
                    'request_id': request_id,
                    'text': text,
                    'status': 'failed',
                    'error': str(e)
                }
        
        # 并发发送请求
        tasks = []
        for i in range(num_requests):
            text = test_texts[i % len(test_texts)]
            tasks.append(send_text_request(None, text, i))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_requests = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
        response_times = [r['response_time_ms'] for r in successful_requests]
        
        if response_times:
            self.results['text_processing'] = {
                'total_requests': num_requests,
                'successful_requests': len(successful_requests),
                'success_rate': len(successful_requests) / num_requests,
                'avg_response_time_ms': statistics.mean(response_times),
                'min_response_time_ms': min(response_times),
                'max_response_time_ms': max(response_times),
                'median_response_time_ms': statistics.median(response_times),
                'throughput_per_second': len(successful_requests) / (max(response_times) / 1000) if response_times else 0
            }
            print(f"✅ 文本处理测试: {len(successful_requests)}/{num_requests} 成功")
            print(f"   平均响应时间: {statistics.mean(response_times):.2f}ms")
            print(f"   吞吐量: {self.results['text_processing']['throughput_per_second']:.2f} 请求/秒")
        else:
            self.results['text_processing'] = {
                'status': 'failed',
                'error': '所有请求都失败了'
            }
            print("❌ 文本处理测试失败")
    
    async def test_cloud_api_performance(self):
        """测试云端API性能"""
        print("测试云端API性能...")
        
        # 测试注册和登录
        async with aiohttp.ClientSession() as session:
            # 注册用户
            register_data = {
                "username": f"test_user_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com",
                "password": "test_password_123"
            }
            
            start_time = time.time()
            async with session.post(f"{self.cloud_url}/auth/register", json=register_data) as response:
                register_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    result = await response.json()
                    access_token = result.get('access_token')
                    
                    # 测试获取用户信息
                    headers = {"Authorization": f"Bearer {access_token}"}
                    start_time = time.time()
                    async with session.get(f"{self.cloud_url}/users/profile", headers=headers) as profile_response:
                        profile_time = (time.time() - start_time) * 1000
                        
                        self.results['cloud_api'] = {
                            'register_time_ms': register_time,
                            'profile_time_ms': profile_time,
                            'status': 'success'
                        }
                        print(f"✅ 云端API测试: 注册 {register_time:.2f}ms, 获取信息 {profile_time:.2f}ms")
                else:
                    self.results['cloud_api'] = {
                        'status': 'failed',
                        'error': f'注册失败: {response.status}'
                    }
                    print(f"❌ 云端API测试失败: {response.status}")
    
    async def test_memory_usage(self):
        """测试内存使用情况"""
        print("测试内存使用情况...")
        
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            
            self.results['memory_usage'] = {
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'status': 'success'
            }
            print(f"✅ 内存使用: RSS {memory_info.rss / 1024 / 1024:.2f}MB, VMS {memory_info.vms / 1024 / 1024:.2f}MB")
        except ImportError:
            self.results['memory_usage'] = {
                'status': 'failed',
                'error': 'psutil未安装'
            }
            print("❌ 无法测试内存使用情况: psutil未安装")
    
    def generate_report(self):
        """生成性能测试报告"""
        print("\n" + "="*60)
        print("性能测试报告")
        print("="*60)
        
        for test_name, result in self.results.items():
            print(f"\n{test_name.upper()}:")
            if result.get('status') == 'success':
                for key, value in result.items():
                    if key != 'status':
                        if isinstance(value, float):
                            print(f"  {key}: {value:.2f}")
                        else:
                            print(f"  {key}: {value}")
            else:
                print(f"  状态: 失败")
                if 'error' in result:
                    print(f"  错误: {result['error']}")
        
        # 保存报告到文件
        with open('performance_report.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n详细报告已保存到: performance_report.json")
    
    async def run_all_tests(self):
        """运行所有性能测试"""
        print("开始性能测试...")
        
        await self.test_backend_health()
        await self.test_websocket_connection(10)
        await self.test_text_processing_performance(20)
        await self.test_cloud_api_performance()
        await self.test_memory_usage()
        
        self.generate_report()

async def main():
    tester = PerformanceTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())

