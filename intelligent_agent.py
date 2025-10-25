#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能Agent - 自研实现
负责：意图理解、任务规划、工具调用、结果汇总
不依赖第三方Agent框架（如LangChain Agent）
"""

import json
import re
from typing import Dict, List, Any, Optional
from baidu_api_client import BaiduAPIClient, BaiduAPIDemoClient


class IntelligentAgent:
    """智能Agent核心类"""
    
    def __init__(self, api_client: BaiduAPIClient = None):
        """
        初始化智能Agent
        
        参数:
            api_client: 百度API客户端实例
        """
        self.api_client = api_client or BaiduAPIDemoClient()
        self.conversation_history = []  # 对话历史
        self.available_tools = self._init_tools()  # 可用工具列表
        
    def _init_tools(self) -> Dict[str, Dict]:
        """
        初始化可用工具
        这里定义了Agent可以调用的所有工具及其描述
        """
        return {
            "open_website": {
                "name": "打开网站",
                "description": "在浏览器中打开指定的网站",
                "parameters": ["url", "target_name"],
                "examples": ["打开GitHub", "访问百度", "浏览谷歌"]
            },
            "play_music": {
                "name": "播放音乐",
                "description": "搜索并播放指定的音乐",
                "parameters": ["song_name", "artist"],
                "examples": ["播放稻香", "放周杰伦的歌", "听音乐"]
            },
            "write_article": {
                "name": "写文章",
                "description": "根据主题生成文章内容",
                "parameters": ["topic", "length"],
                "examples": ["写一篇关于AI的文章", "创作科技主题的内容"]
            },
            "generate_code": {
                "name": "生成代码",
                "description": "根据需求生成代码片段",
                "parameters": ["language", "requirements"],
                "examples": ["写一个Python函数", "生成JavaScript代码"]
            },
            "web_search": {
                "name": "网络搜索",
                "description": "在互联网上搜索信息",
                "parameters": ["query"],
                "examples": ["搜索Python教程", "查询天气"]
            },
            "file_operation": {
                "name": "文件操作",
                "description": "创建、读取或修改文件",
                "parameters": ["operation", "file_path", "content"],
                "examples": ["创建一个文件", "保存内容到文件"]
            },
            "system_control": {
                "name": "系统控制",
                "description": "控制系统功能（音量、亮度等）",
                "parameters": ["action", "value"],
                "examples": ["调高音量", "调整屏幕亮度"]
            }
        }
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        处理用户输入的主流程
        
        流程:
        1. 理解用户意图（调用LLM）
        2. 规划任务步骤
        3. 执行工具调用
        4. 汇总结果
        
        参数:
            user_input: 用户的文本输入
        
        返回:
            执行结果字典
        """
        print(f"\n{'='*60}")
        print(f"🎯 用户输入: {user_input}")
        print(f"{'='*60}")
        
        # 步骤1: 意图理解
        intent_result = self._understand_intent(user_input)
        print(f"📊 意图分析: {json.dumps(intent_result, ensure_ascii=False, indent=2)}")
        
        if not intent_result.get("success"):
            return {
                "success": False,
                "error": "意图理解失败",
                "message": "抱歉，我没有理解您的意思"
            }
        
        # 步骤2: 任务规划
        plan = self._plan_tasks(intent_result)
        print(f"📋 任务规划: {json.dumps(plan, ensure_ascii=False, indent=2)}")
        
        # 步骤3: 执行任务
        execution_result = self._execute_plan(plan, user_input)
        print(f"✅ 执行结果: {json.dumps(execution_result, ensure_ascii=False, indent=2)}")
        
        # 步骤4: 添加到对话历史
        self.conversation_history.append({
            "user": user_input,
            "agent": execution_result.get("message", ""),
            "intent": intent_result,
            "plan": plan
        })
        
        return execution_result
    
    def _understand_intent(self, user_input: str) -> Dict[str, Any]:
        """
        理解用户意图
        使用LLM进行深度语义理解
        
        返回:
            {
                "success": True/False,
                "action": "动作类型",
                "parameters": {参数字典},
                "confidence": 置信度
            }
        """
        # 构造prompt，让LLM理解用户意图并返回结构化数据
        prompt = f"""你是一个智能助手的意图理解模块。请分析用户的指令，返回JSON格式的结果。

可用的工具有:
{json.dumps(self.available_tools, ensure_ascii=False, indent=2)}

用户指令: {user_input}

请分析用户意图，返回JSON格式（只返回JSON，不要其他内容）:
{{
    "action": "工具名称(从上面的工具列表中选择)",
    "parameters": {{"参数名": "参数值"}},
    "reasoning": "为什么选择这个工具"
}}"""
        
        # 调用LLM
        llm_result = self.api_client.chat(prompt)
        
        if not llm_result.get("success"):
            # LLM调用失败，使用备用规则
            return self._fallback_intent_understanding(user_input)
        
        try:
            # 解析LLM返回的JSON
            content = llm_result.get("content", "")
            
            # 尝试提取JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                intent_data = json.loads(json_match.group())
                action = intent_data.get("action")
                parameters = intent_data.get("parameters", {})
                
                # 如果parameters为空，尝试从intent_data的其他字段提取
                if not parameters:
                    for key, value in intent_data.items():
                        if key not in ['action', 'reasoning', 'confidence']:
                            parameters[key] = value
                
                return {
                    "success": True,
                    "action": action,
                    "parameters": parameters,
                    "reasoning": intent_data.get("reasoning", ""),
                    "confidence": 0.9
                }
            else:
                # JSON解析失败，使用备用方案
                return self._fallback_intent_understanding(user_input)
                
        except Exception as e:
            print(f"⚠️  意图解析异常: {e}")
            return self._fallback_intent_understanding(user_input)
    
    def _fallback_intent_understanding(self, user_input: str) -> Dict[str, Any]:
        """
        备用的意图理解（基于规则）
        当LLM调用失败时使用
        """
        user_input_lower = user_input.lower()
        
        # 打开网站
        if "打开" in user_input or "访问" in user_input or "浏览" in user_input:
            target = ""
            url = ""
            
            if "github" in user_input_lower:
                target = "GitHub"
                url = "https://github.com"
            elif "百度" in user_input or "baidu" in user_input_lower:
                target = "百度"
                url = "https://www.baidu.com"
            elif "谷歌" in user_input or "google" in user_input_lower:
                target = "谷歌"
                url = "https://www.google.com"
            
            if url:
                return {
                    "success": True,
                    "action": "open_website",
                    "parameters": {"url": url, "target_name": target},
                    "confidence": 0.8,
                    "url": url,
                    "target_name": target
                }
        
        # 播放音乐
        if "播放" in user_input or "音乐" in user_input or "听" in user_input or "歌" in user_input:
            song_name = "未指定"
            artist = ""
            
            # 尝试提取歌曲名和歌手
            if "的" in user_input:
                parts = user_input.split("的")
                if len(parts) >= 2:
                    artist = parts[0].replace("播放", "").replace("听", "").strip()
                    song_name = parts[1].strip()
            
            return {
                "success": True,
                "action": "play_music",
                "parameters": {"song_name": song_name, "artist": artist},
                "confidence": 0.8
            }
        
        # 写文章
        if "写" in user_input or "创作" in user_input or "文章" in user_input:
            topic = "未指定主题"
            if "关于" in user_input:
                parts = user_input.split("关于")
                if len(parts) > 1:
                    topic = parts[1].split("的")[0].strip()
            
            return {
                "success": True,
                "action": "write_article",
                "parameters": {"topic": topic, "length": "medium"},
                "confidence": 0.7
            }
        
        # 生成代码
        if "代码" in user_input or "编程" in user_input or "程序" in user_input:
            return {
                "success": True,
                "action": "generate_code",
                "parameters": {"requirements": user_input},
                "confidence": 0.7
            }
        
        # 搜索
        if "搜索" in user_input or "查询" in user_input or "查找" in user_input:
            query = user_input.replace("搜索", "").replace("查询", "").replace("查找", "").strip()
            return {
                "success": True,
                "action": "web_search",
                "parameters": {"query": query},
                "confidence": 0.7
            }
        
        # 默认响应
        return {
            "success": True,
            "action": "general_response",
            "parameters": {"message": user_input},
            "confidence": 0.5
        }
    
    def _plan_tasks(self, intent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        任务规划
        将用户意图转换为具体的执行计划
        """
        action = intent_result.get("action")
        parameters = intent_result.get("parameters", {})
        
        # 简单任务：单步执行
        if action in ["open_website", "play_music", "web_search"]:
            return {
                "type": "simple",
                "steps": [
                    {
                        "tool": action,
                        "parameters": parameters,
                        "description": f"执行{self.available_tools.get(action, {}).get('name', action)}"
                    }
                ]
            }
        
        # 复杂任务：多步执行
        elif action in ["write_article", "generate_code"]:
            return {
                "type": "complex",
                "steps": [
                    {
                        "tool": "prepare_content",
                        "parameters": parameters,
                        "description": "准备内容素材"
                    },
                    {
                        "tool": action,
                        "parameters": parameters,
                        "description": f"生成{self.available_tools.get(action, {}).get('name', action)}"
                    },
                    {
                        "tool": "file_operation",
                        "parameters": {"operation": "save"},
                        "description": "保存结果到文件"
                    }
                ]
            }
        
        # 默认计划
        else:
            return {
                "type": "simple",
                "steps": [
                    {
                        "tool": action,
                        "parameters": parameters,
                        "description": "执行用户指令"
                    }
                ]
            }
    
    def _execute_plan(self, plan: Dict[str, Any], original_input: str) -> Dict[str, Any]:
        """
        执行任务计划
        """
        steps = plan.get("steps", [])
        results = []
        
        for step in steps:
            tool = step.get("tool")
            parameters = step.get("parameters", {})
            
            # 执行工具
            step_result = self._execute_tool(tool, parameters, original_input)
            results.append(step_result)
            
            # 如果某一步失败，停止执行
            if not step_result.get("success"):
                break
        
        # 汇总结果
        if results and results[-1].get("success"):
            return results[-1]
        else:
            return {
                "success": False,
                "message": "任务执行失败",
                "details": results
            }
    
    def _execute_tool(self, tool: str, parameters: Dict, original_input: str) -> Dict[str, Any]:
        """
        执行具体工具
        这里返回执行指令，实际执行由SystemController完成
        """
        # 返回工具调用结果（结构化数据）
        return {
            "success": True,
            "tool": tool,
            "action": tool,
            "parameters": parameters,
            "message": f"准备执行: {self.available_tools.get(tool, {}).get('name', tool)}",
            "original_input": original_input
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """获取对话历史"""
        return self.conversation_history
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("智能Agent测试")
    print("=" * 60)
    
    agent = IntelligentAgent()
    
    # 测试用例
    test_cases = [
        "帮我打开GitHub网站",
        "播放周杰伦的稻香",
        "写一篇关于人工智能的文章",
        "搜索Python教程"
    ]
    
    for test_input in test_cases:
        result = agent.process_user_input(test_input)
        print(f"\n最终结果: {result.get('message')}\n")

