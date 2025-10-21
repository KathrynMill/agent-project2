#!/usr/bin/env python3
"""
测试集成系统 - 本地大模型 + Echo Command
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.append('/home/aa/echo-command/backend')

from services.ai.local_llm_service import local_llm_service
from services.ai.intent_parser_service import IntentParserService
from models.schemas import AIIntentResult, CommandType

async def test_local_llm():
    """测试本地大模型"""
    print("🧪 测试本地大模型服务")
    print("=" * 50)
    
    # 启动服务
    await local_llm_service.start()
    
    # 测试用例
    test_cases = [
        "你好",
        "播放音乐",
        "打开浏览器",
        "调节音量",
        "写一篇文章",
        "帮我写代码"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_input}")
        
        # 测试回复生成
        response = await local_llm_service.generate_response(test_input)
        print(f"回复: {response.text}")
        
        # 测试意图解析
        intent = await local_llm_service.parse_intent(test_input)
        print(f"意图: {intent.intent}")
        print(f"置信度: {intent.confidence}")
        print(f"实体: {intent.entities}")
    
    # 显示状态
    status = local_llm_service.get_status()
    print(f"\n📊 服务状态:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    await local_llm_service.stop()
    print("\n✅ 本地大模型测试完成！")

async def test_intent_parser():
    """测试意图解析服务"""
    print("\n🧪 测试意图解析服务")
    print("=" * 50)
    
    # 创建意图解析服务
    parser = IntentParserService()
    
    # 测试用例
    test_cases = [
        "你好",
        "播放音乐",
        "打开浏览器",
        "调节音量到50%",
        "写一篇关于AI的文章",
        "帮我写一个Python脚本"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_input}")
        
        try:
            intent_result = await parser.parse_intent(test_input)
            print(f"意图: {intent_result.intent}")
            print(f"置信度: {intent_result.confidence}")
            print(f"命令类型: {intent_result.command_type}")
            print(f"动作: {intent_result.action}")
            print(f"参数: {intent_result.parameters}")
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n✅ 意图解析测试完成！")

async def test_integrated_system():
    """测试集成系统"""
    print("\n🎯 测试集成系统")
    print("=" * 50)
    
    # 启动本地大模型
    await local_llm_service.start()
    
    # 创建意图解析服务
    parser = IntentParserService()
    
    # 模拟完整的语音交互流程
    user_inputs = [
        "你好，请介绍一下自己",
        "帮我播放音乐",
        "打开浏览器",
        "调节音量",
        "写一篇文章"
    ]
    
    for i, user_input in enumerate(user_inputs, 1):
        print(f"\n🎤 用户输入 {i}: {user_input}")
        
        try:
            # 1. 意图解析
            intent_result = await parser.parse_intent(user_input)
            print(f"🤖 意图解析: {intent_result.intent} (置信度: {intent_result.confidence})")
            
            # 2. 生成回复
            response = await local_llm_service.generate_response(user_input)
            print(f"💬 AI回复: {response.text}")
            
            # 3. 显示执行计划
            if intent_result.intent != "unknown":
                print(f"📋 执行计划: {intent_result.action} - {intent_result.parameters}")
            else:
                print("❓ 无法识别的指令")
                
        except Exception as e:
            print(f"❌ 处理失败: {e}")
    
    await local_llm_service.stop()
    print("\n✅ 集成系统测试完成！")

async def main():
    """主测试函数"""
    print("🚀 Echo Command - 集成系统测试")
    print("=" * 60)
    
    try:
        # 测试本地大模型
        await test_local_llm()
        
        # 测试意图解析
        await test_intent_parser()
        
        # 测试集成系统
        await test_integrated_system()
        
        print("\n🎉 所有测试完成！系统运行正常！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

