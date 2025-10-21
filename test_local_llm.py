#!/usr/bin/env python3
"""
测试本地大模型功能
"""

from simple_local_llm import LocalLLMService

def test_local_llm():
    """测试本地大模型"""
    print("🎯 Echo Command - 本地大模型测试")
    print("=" * 50)
    
    # 创建服务
    service = LocalLLMService()
    service.start()
    
    # 测试用例
    test_cases = [
        "你好",
        "播放音乐",
        "打开浏览器", 
        "调节音量",
        "写一篇文章",
        "帮我写代码"
    ]
    
    print("\n🧪 开始功能测试:")
    print("-" * 50)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_input}")
        response = service.chat(test_input)
        print(f"回复: {response}")
    
    # 显示服务状态
    print(f"\n📊 服务状态:")
    status = service.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    service.stop()
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    test_local_llm()

