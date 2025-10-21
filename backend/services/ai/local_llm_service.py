"""
本地大模型服务
基于简化的规则引擎，适合您的5.3GB内存配置
"""

import asyncio
import json
import re
import random
from typing import Dict, List, Optional, Any
from loguru import logger

from models.schemas import AIResponseResult, AIIntentResult


class LocalLLMService:
    """本地大模型服务类"""
    
    def __init__(self):
        self.model_name = "SimpleLocalLLM-1.0"
        self.context = []
        self.max_context = 10
        self.is_running = False
        
    async def start(self):
        """启动服务"""
        self.is_running = True
        logger.info("🚀 本地大模型服务已启动")
        logger.info(f"📊 模型: {self.model_name}")
        logger.info(f"💾 内存使用: 约50MB")
        
    async def stop(self):
        """停止服务"""
        self.is_running = False
        logger.info("🛑 本地大模型服务已停止")
        
    async def generate_response(self, prompt: str, context: Optional[List[Dict]] = None) -> AIResponseResult:
        """生成回复"""
        try:
            # 基于规则的回复生成
            response_text = self._rule_based_response(prompt)
            
            # 保存到上下文
            self.context.append({"user": prompt, "assistant": response_text})
            if len(self.context) > self.max_context:
                self.context.pop(0)
            
            return AIResponseResult(
                text=response_text,
                confidence=0.9,
                model=self.model_name,
                usage={
                    "prompt_tokens": len(prompt.split()),
                    "completion_tokens": len(response_text.split()),
                    "total_tokens": len(prompt.split()) + len(response_text.split())
                }
            )
            
        except Exception as e:
            logger.error(f"本地大模型生成回复失败: {e}")
            return AIResponseResult(
                text="抱歉，我暂时无法处理您的请求。",
                confidence=0.1,
                model=self.model_name,
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            )
    
    async def parse_intent(self, text: str) -> AIIntentResult:
        """解析用户意图"""
        try:
            intent = self._parse_intent_rules(text)
            
            return AIIntentResult(
                intent=intent["intent"],
                entities=intent["entities"],
                confidence=intent["confidence"],
                model=self.model_name
            )
            
        except Exception as e:
            logger.error(f"意图解析失败: {e}")
            return AIIntentResult(
                intent="unknown",
                entities={},
                confidence=0.1,
                model=self.model_name
            )
    
    def _rule_based_response(self, prompt: str) -> str:
        """基于规则的回复生成"""
        prompt_lower = prompt.lower()
        
        # 问候语
        if any(word in prompt_lower for word in ["你好", "hello", "hi", "嗨"]):
            return "你好！我是Echo Command的AI助手，可以帮助您控制电脑。请告诉我您需要什么帮助？"
        
        # 系统控制指令
        if "播放音乐" in prompt or "play music" in prompt_lower:
            return "好的，我来帮您播放音乐。正在打开音乐播放器..."
        
        if "打开浏览器" in prompt or "open browser" in prompt_lower:
            return "好的，正在为您打开浏览器..."
        
        if "调节音量" in prompt or "volume" in prompt_lower:
            return "好的，我来帮您调节音量。请告诉我要调节到多少？"
        
        if "写文章" in prompt or "write" in prompt_lower:
            return "好的，我来帮您写文章。请告诉我文章的主题和内容要求。"
        
        # 编程相关
        if "代码" in prompt or "code" in prompt_lower:
            return "我可以帮您编写代码。请告诉我您需要什么类型的代码？"
        
        # 默认回复
        responses = [
            "我理解您的需求，正在为您处理...",
            "好的，我来帮您完成这个任务。",
            "请稍等，我正在分析您的请求...",
            "我明白了，让我为您执行这个操作。"
        ]
        return random.choice(responses)
    
    def _parse_intent_rules(self, text: str) -> Dict[str, Any]:
        """基于规则的意图解析"""
        text_lower = text.lower()
        
        # 系统控制意图
        if any(word in text_lower for word in ["播放", "play", "音乐", "music"]):
            return {
                "intent": "play_music",
                "entities": {"action": "play", "target": "music"},
                "confidence": 0.9
            }
        
        if any(word in text_lower for word in ["打开", "open", "浏览器", "browser"]):
            return {
                "intent": "open_browser",
                "entities": {"action": "open", "target": "browser"},
                "confidence": 0.9
            }
        
        if any(word in text_lower for word in ["音量", "volume", "声音", "sound"]):
            return {
                "intent": "adjust_volume",
                "entities": {"action": "adjust", "target": "volume"},
                "confidence": 0.9
            }
        
        if any(word in text_lower for word in ["写", "write", "文章", "article"]):
            return {
                "intent": "write_article",
                "entities": {"action": "write", "target": "article"},
                "confidence": 0.9
            }
        
        if any(word in text_lower for word in ["代码", "code", "编程", "programming"]):
            return {
                "intent": "write_code",
                "entities": {"action": "write", "target": "code"},
                "confidence": 0.9
            }
        
        # 问候意图
        if any(word in text_lower for word in ["你好", "hello", "hi", "嗨"]):
            return {
                "intent": "greeting",
                "entities": {"action": "greet"},
                "confidence": 0.9
            }
        
        # 默认意图
        return {
            "intent": "general",
            "entities": {},
            "confidence": 0.5
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取服务状态"""
        return {
            "running": self.is_running,
            "model": self.model_name,
            "context_length": len(self.context),
            "memory_usage": "约50MB"
        }
    
    def clear_context(self):
        """清空上下文"""
        self.context = []
        logger.info("上下文已清空")


# 全局服务实例
local_llm_service = LocalLLMService()

