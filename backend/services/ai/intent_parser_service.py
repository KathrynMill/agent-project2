"""
意图解析服务 - 使用GPT-4o进行意图理解和命令生成
"""
import json
from typing import Dict, Any, List
import openai
from loguru import logger

from models.schemas import AIIntentResult, CommandType, SystemAction, FileAction, TextAction
from config.settings import settings


class IntentParserService:
    """意图解析服务类"""
    
    def __init__(self):
        """初始化意图解析服务"""
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self._setup_functions()
    
    def _setup_functions(self):
        """设置函数调用定义"""
        self.functions = [
            {
                "name": "execute_system_control",
                "description": "执行系统控制操作，如音量调节、应用开关等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [action.value for action in SystemAction],
                            "description": "系统操作类型"
                        },
                        "target": {
                            "type": "string",
                            "description": "操作目标，如应用名称、音量值等"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "额外参数"
                        }
                    },
                    "required": ["action"]
                }
            },
            {
                "name": "execute_file_operation",
                "description": "执行文件操作，如创建、读取、写入、删除文件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [action.value for action in FileAction],
                            "description": "文件操作类型"
                        },
                        "file_path": {
                            "type": "string",
                            "description": "文件路径"
                        },
                        "content": {
                            "type": "string",
                            "description": "文件内容（写入时使用）"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "额外参数"
                        }
                    },
                    "required": ["action"]
                }
            },
            {
                "name": "execute_text_processing",
                "description": "执行文本处理操作，如写文章、总结、翻译等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": [action.value for action in TextAction],
                            "description": "文本处理类型"
                        },
                        "text": {
                            "type": "string",
                            "description": "要处理的文本内容"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "处理参数，如主题、长度、语言等"
                        }
                    },
                    "required": ["action"]
                }
            },
            {
                "name": "execute_application_control",
                "description": "执行应用程序控制，如打开特定应用",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {
                            "type": "string",
                            "description": "应用程序名称"
                        },
                        "action": {
                            "type": "string",
                            "enum": ["open", "close", "minimize", "maximize"],
                            "description": "应用操作类型"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "额外参数"
                        }
                    },
                    "required": ["app_name", "action"]
                }
            },
            {
                "name": "execute_media_control",
                "description": "执行媒体控制，如播放音乐、视频等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["play", "pause", "stop", "next", "previous", "volume"],
                            "description": "媒体操作类型"
                        },
                        "media_path": {
                            "type": "string",
                            "description": "媒体文件路径或URL"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "额外参数"
                        }
                    },
                    "required": ["action"]
                }
            },
            {
                "name": "execute_query",
                "description": "执行查询操作，如获取系统信息、天气等",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query_type": {
                            "type": "string",
                            "enum": ["system_info", "weather", "time", "date", "processes"],
                            "description": "查询类型"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "查询参数"
                        }
                    },
                    "required": ["query_type"]
                }
            }
        ]
    
    async def parse_intent(self, text: str, context: Dict[str, Any] = None) -> AIIntentResult:
        """
        解析用户意图
        
        Args:
            text: 用户输入的文本
            context: 上下文信息
            
        Returns:
            AIIntentResult: 意图解析结果
        """
        try:
            # 构建提示词
            system_prompt = self._build_system_prompt(context)
            
            # 调用GPT-4o进行意图解析
            response = await self._call_gpt(text, system_prompt)
            
            # 解析响应
            return self._parse_response(response, text)
            
        except Exception as e:
            logger.error(f"Intent parsing failed: {e}")
            return AIIntentResult(
                intent="unknown",
                confidence=0.0,
                entities={},
                command_type=CommandType.SYSTEM_CONTROL,
                action="unknown",
                parameters={}
            )
    
    def _build_system_prompt(self, context: Dict[str, Any] = None) -> str:
        """构建系统提示词"""
        prompt = """你是一个智能语音助手，负责理解用户的语音指令并转换为可执行的命令。

你的任务：
1. 理解用户的自然语言指令
2. 识别指令的意图和参数
3. 调用相应的函数来执行操作

支持的指令类型：
- 系统控制：音量调节、屏幕截图、锁屏等
- 文件操作：创建、读取、写入、删除文件
- 文本处理：写文章、总结、翻译等
- 应用控制：打开、关闭应用程序
- 媒体控制：播放音乐、视频等
- 信息查询：系统信息、天气、时间等

请根据用户的指令，选择合适的函数并提取相关参数。"""
        
        if context:
            prompt += f"\n\n当前上下文：{json.dumps(context, ensure_ascii=False)}"
        
        return prompt
    
    async def _call_gpt(self, text: str, system_prompt: str) -> Dict[str, Any]:
        """调用GPT-4o API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                functions=self.functions,
                function_call="auto",
                temperature=0.1
            )
            
            return response.choices[0].message
            
        except Exception as e:
            logger.error(f"GPT API call failed: {e}")
            raise
    
    def _parse_response(self, response: Dict[str, Any], original_text: str) -> AIIntentResult:
        """解析GPT响应"""
        try:
            if response.function_call:
                function_name = response.function_call.name
                function_args = json.loads(response.function_call.arguments)
                
                # 根据函数名确定命令类型
                command_type = self._get_command_type_from_function(function_name)
                action = function_args.get("action", "unknown")
                
                return AIIntentResult(
                    intent=function_name,
                    confidence=0.9,  # GPT-4o的置信度较高
                    entities=function_args,
                    command_type=command_type,
                    action=action,
                    parameters=function_args
                )
            else:
                # 如果没有函数调用，尝试从文本中提取意图
                return self._fallback_intent_parsing(original_text)
                
        except Exception as e:
            logger.error(f"Response parsing failed: {e}")
            return AIIntentResult(
                intent="unknown",
                confidence=0.0,
                entities={},
                command_type=CommandType.SYSTEM_CONTROL,
                action="unknown",
                parameters={}
            )
    
    def _get_command_type_from_function(self, function_name: str) -> CommandType:
        """根据函数名获取命令类型"""
        function_mapping = {
            "execute_system_control": CommandType.SYSTEM_CONTROL,
            "execute_file_operation": CommandType.FILE_OPERATION,
            "execute_text_processing": CommandType.TEXT_PROCESSING,
            "execute_application_control": CommandType.APPLICATION,
            "execute_media_control": CommandType.MEDIA,
            "execute_query": CommandType.QUERY
        }
        return function_mapping.get(function_name, CommandType.SYSTEM_CONTROL)
    
    def _fallback_intent_parsing(self, text: str) -> AIIntentResult:
        """备用意图解析（基于关键词匹配）"""
        text_lower = text.lower()
        
        # 简单的关键词匹配
        if any(keyword in text_lower for keyword in ["音量", "声音", "volume"]):
            return AIIntentResult(
                intent="volume_control",
                confidence=0.7,
                entities={"text": text},
                command_type=CommandType.SYSTEM_CONTROL,
                action="volume_set",
                parameters={"text": text}
            )
        elif any(keyword in text_lower for keyword in ["打开", "启动", "open", "launch"]):
            return AIIntentResult(
                intent="open_application",
                confidence=0.7,
                entities={"text": text},
                command_type=CommandType.APPLICATION,
                action="open",
                parameters={"text": text}
            )
        else:
            return AIIntentResult(
                intent="unknown",
                confidence=0.3,
                entities={"text": text},
                command_type=CommandType.SYSTEM_CONTROL,
                action="unknown",
                parameters={"text": text}
            )

