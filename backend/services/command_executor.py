"""
命令执行器
"""
import asyncio
import time
from typing import Dict, Any, Optional
from loguru import logger

from models.schemas import CommandResult, AIIntentResult, CommandType
from services.system.controller_factory import ControllerFactory
from services.ai.tts_service import TTSService


class CommandExecutor:
    """命令执行器类"""
    
    def __init__(self):
        """初始化命令执行器"""
        self.system_controller = ControllerFactory.create_controller()
        self.tts_service = TTSService()
        self.execution_history = []
    
    async def execute_intent(self, intent_result: AIIntentResult, session_id: str = None) -> CommandResult:
        """
        执行AI解析的意图
        
        Args:
            intent_result: AI意图解析结果
            session_id: 会话ID
            
        Returns:
            CommandResult: 执行结果
        """
        start_time = time.time()
        
        try:
            logger.info(f"Executing intent: {intent_result.intent}, action: {intent_result.action}")
            
            # 根据命令类型执行相应操作
            if intent_result.command_type == CommandType.SYSTEM_CONTROL:
                result = await self._execute_system_control(intent_result)
            elif intent_result.command_type == CommandType.FILE_OPERATION:
                result = await self._execute_file_operation(intent_result)
            elif intent_result.command_type == CommandType.TEXT_PROCESSING:
                result = await self._execute_text_processing(intent_result)
            elif intent_result.command_type == CommandType.APPLICATION:
                result = await self._execute_application_control(intent_result)
            elif intent_result.command_type == CommandType.MEDIA:
                result = await self._execute_media_control(intent_result)
            elif intent_result.command_type == CommandType.QUERY:
                result = await self._execute_query(intent_result)
            else:
                result = CommandResult(
                    success=False,
                    message=f"Unknown command type: {intent_result.command_type}",
                    execution_time=time.time() - start_time
                )
            
            # 记录执行历史
            self._record_execution(intent_result, result, session_id)
            
            return result
            
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            result = CommandResult(
                success=False,
                message=f"Command execution failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
            self._record_execution(intent_result, result, session_id)
            return result
    
    async def _execute_system_control(self, intent_result: AIIntentResult) -> CommandResult:
        """执行系统控制命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "volume_up":
            amount = parameters.get("amount", 10)
            return await self.system_controller.volume_up(amount)
        elif action == "volume_down":
            amount = parameters.get("amount", 10)
            return await self.system_controller.volume_down(amount)
        elif action == "volume_set":
            volume = parameters.get("volume", 50)
            return await self.system_controller.volume_set(volume)
        elif action == "mute":
            return await self.system_controller.mute()
        elif action == "unmute":
            return await self.system_controller.unmute()
        elif action == "screenshot":
            save_path = parameters.get("save_path")
            return await self.system_controller.screenshot(save_path)
        elif action == "lock_screen":
            return await self.system_controller.lock_screen()
        else:
            return CommandResult(
                success=False,
                message=f"Unknown system control action: {action}",
                execution_time=0.0
            )
    
    async def _execute_file_operation(self, intent_result: AIIntentResult) -> CommandResult:
        """执行文件操作命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "create_file":
            file_path = parameters.get("file_path")
            content = parameters.get("content", "")
            return await self.system_controller.create_file(file_path, content)
        elif action == "read_file":
            file_path = parameters.get("file_path")
            return await self.system_controller.read_file(file_path)
        elif action == "write_file":
            file_path = parameters.get("file_path")
            content = parameters.get("content", "")
            return await self.system_controller.write_file(file_path, content)
        elif action == "delete_file":
            file_path = parameters.get("file_path")
            return await self.system_controller.delete_file(file_path)
        elif action == "list_files":
            directory = parameters.get("directory", ".")
            return await self.system_controller.list_files(directory)
        else:
            return CommandResult(
                success=False,
                message=f"Unknown file operation action: {action}",
                execution_time=0.0
            )
    
    async def _execute_text_processing(self, intent_result: AIIntentResult) -> CommandResult:
        """执行文本处理命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "write_article":
            topic = parameters.get("topic", "未指定主题")
            length = parameters.get("length", 500)
            
            # 这里可以调用AI服务生成文章
            article_content = await self._generate_article(topic, length)
            
            # 保存到文件
            file_path = f"/tmp/article_{int(time.time())}.txt"
            result = await self.system_controller.write_file(file_path, article_content)
            
            if result.success:
                result.message = f"文章已生成并保存到: {file_path}"
                result.output = article_content
            
            return result
        
        elif action == "summarize":
            text = parameters.get("text", "")
            if not text:
                return CommandResult(
                    success=False,
                    message="没有提供要总结的文本",
                    execution_time=0.0
                )
            
            # 这里可以调用AI服务进行总结
            summary = await self._summarize_text(text)
            
            return CommandResult(
                success=True,
                message="文本总结完成",
                execution_time=0.0,
                output=summary
            )
        
        else:
            return CommandResult(
                success=False,
                message=f"Unknown text processing action: {action}",
                execution_time=0.0
            )
    
    async def _execute_application_control(self, intent_result: AIIntentResult) -> CommandResult:
        """执行应用控制命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "open":
            app_name = parameters.get("app_name")
            if not app_name:
                return CommandResult(
                    success=False,
                    message="未指定应用程序名称",
                    execution_time=0.0
                )
            
            return await self.system_controller.open_application(app_name, parameters)
        
        elif action == "close":
            app_name = parameters.get("app_name")
            if not app_name:
                return CommandResult(
                    success=False,
                    message="未指定应用程序名称",
                    execution_time=0.0
                )
            
            return await self.system_controller.close_application(app_name)
        
        else:
            return CommandResult(
                success=False,
                message=f"Unknown application action: {action}",
                execution_time=0.0
            )
    
    async def _execute_media_control(self, intent_result: AIIntentResult) -> CommandResult:
        """执行媒体控制命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "play":
            media_path = parameters.get("media_path")
            if not media_path:
                return CommandResult(
                    success=False,
                    message="未指定媒体文件路径",
                    execution_time=0.0
                )
            
            return await self.system_controller.play_media(media_path)
        
        elif action == "pause":
            return await self.system_controller.pause_media()
        
        elif action == "stop":
            return await self.system_controller.stop_media()
        
        else:
            return CommandResult(
                success=False,
                message=f"Unknown media action: {action}",
                execution_time=0.0
            )
    
    async def _execute_query(self, intent_result: AIIntentResult) -> CommandResult:
        """执行查询命令"""
        action = intent_result.action
        parameters = intent_result.parameters
        
        if action == "time":
            return await self.system_controller.get_time()
        
        elif action == "date":
            return await self.system_controller.get_date()
        
        elif action == "weather":
            location = parameters.get("location")
            return await self.system_controller.get_weather(location)
        
        elif action == "processes":
            return await self.system_controller.get_processes()
        
        else:
            return CommandResult(
                success=False,
                message=f"Unknown query action: {action}",
                execution_time=0.0
            )
    
    async def _generate_article(self, topic: str, length: int) -> str:
        """生成文章（简化版本）"""
        # 这里应该调用AI服务生成文章
        # 现在返回一个简单的模板
        return f"""
# {topic}

这是一篇关于{topic}的文章。

## 引言

{topic}是一个重要的话题，值得我们深入探讨。

## 主要内容

在这篇文章中，我们将从多个角度来分析{topic}：

1. 基本概念
2. 历史发展
3. 现状分析
4. 未来展望

## 结论

通过以上分析，我们可以看出{topic}的重要性和发展前景。

---
*本文由Echo Command AI助手生成*
"""
    
    async def _summarize_text(self, text: str) -> str:
        """总结文本（简化版本）"""
        # 这里应该调用AI服务进行总结
        # 现在返回一个简单的总结
        words = text.split()
        if len(words) <= 50:
            return text
        
        # 简单截取前50个词作为总结
        summary_words = words[:50]
        return " ".join(summary_words) + "..."
    
    def _record_execution(self, intent_result: AIIntentResult, result: CommandResult, session_id: str = None):
        """记录执行历史"""
        execution_record = {
            "timestamp": time.time(),
            "session_id": session_id,
            "intent": intent_result.intent,
            "action": intent_result.action,
            "command_type": intent_result.command_type,
            "success": result.success,
            "execution_time": result.execution_time,
            "message": result.message
        }
        
        self.execution_history.append(execution_record)
        
        # 保持历史记录在合理范围内
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-500:]
    
    def get_execution_history(self, session_id: str = None, limit: int = 100) -> list:
        """
        获取执行历史
        
        Args:
            session_id: 会话ID（可选）
            limit: 限制返回数量
            
        Returns:
            list: 执行历史列表
        """
        history = self.execution_history
        
        if session_id:
            history = [record for record in history if record.get("session_id") == session_id]
        
        return history[-limit:] if limit > 0 else history
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for record in self.execution_history if record["success"])
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "average_execution_time": sum(record["execution_time"] for record in self.execution_history) / total_executions if total_executions > 0 else 0
        }

