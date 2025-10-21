#!/usr/bin/env python3
"""
Echo Command 系统测试脚本
"""
import asyncio
import json
import time
import requests
from pathlib import Path

def test_backend_health():
    """测试后端健康状态"""
    print("测试后端健康状态...")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 后端健康检查通过: {data}")
            return True
        else:
            print(f"❌ 后端健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端连接失败: {e}")
        return False

def test_websocket_connection():
    """测试WebSocket连接"""
    print("测试WebSocket连接...")
    try:
        import websocket
        
        def on_message(ws, message):
            print(f"收到消息: {message}")
            ws.close()
        
        def on_error(ws, error):
            print(f"WebSocket错误: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print("WebSocket连接关闭")
        
        def on_open(ws):
            print("WebSocket连接已建立")
            # 发送测试消息
            test_message = {
                "type": "text",
                "text": "测试消息",
                "session_id": None
            }
            ws.send(json.dumps(test_message))
        
        ws = websocket.WebSocketApp(
            "ws://127.0.0.1:8000/ws",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        ws.run_forever()
        print("✅ WebSocket连接测试完成")
        return True
        
    except ImportError:
        print("❌ 缺少websocket-client库，请安装: pip install websocket-client")
        return False
    except Exception as e:
        print(f"❌ WebSocket连接测试失败: {e}")
        return False

def test_ai_services():
    """测试AI服务"""
    print("测试AI服务...")
    
    # 检查环境变量
    import os
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ 未设置OPENAI_API_KEY环境变量")
        return False
    
    try:
        # 测试OpenAI连接
        import openai
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 简单测试
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API连接正常")
        return True
        
    except Exception as e:
        print(f"❌ AI服务测试失败: {e}")
        return False

def test_system_controller():
    """测试系统控制器"""
    print("测试系统控制器...")
    
    try:
        import sys
        sys.path.append(str(Path(__file__).parent / "backend"))
        
        from services.system.controller_factory import ControllerFactory
        
        controller = ControllerFactory.create_controller()
        print(f"✅ 系统控制器创建成功: {type(controller).__name__}")
        
        # 测试获取系统信息
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        system_info = loop.run_until_complete(controller.get_system_info())
        print(f"✅ 系统信息获取成功: {system_info.os_name} {system_info.os_version}")
        
        loop.close()
        return True
        
    except Exception as e:
        print(f"❌ 系统控制器测试失败: {e}")
        return False

def test_frontend_build():
    """测试前端构建"""
    print("测试前端构建...")
    
    frontend_path = Path(__file__).parent / "frontend"
    if not frontend_path.exists():
        print("❌ 前端目录不存在")
        return False
    
    package_json = frontend_path / "package.json"
    if not package_json.exists():
        print("❌ package.json不存在")
        return False
    
    print("✅ 前端项目结构正常")
    return True

def main():
    """主测试函数"""
    print("=" * 50)
    print("Echo Command 系统测试")
    print("=" * 50)
    
    tests = [
        ("后端健康检查", test_backend_health),
        ("WebSocket连接", test_websocket_connection),
        ("AI服务", test_ai_services),
        ("系统控制器", test_system_controller),
        ("前端构建", test_frontend_build),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)



