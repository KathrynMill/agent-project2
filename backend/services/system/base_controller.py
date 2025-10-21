"""
系统控制器基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from loguru import logger

from models.schemas import CommandResult, SystemInfo


class BaseController(ABC):
    """系统控制器基类"""
    
    def __init__(self):
        """初始化控制器"""
        self.safety_enabled = True
        self.command_delay = 0.1
    
    @abstractmethod
    async def execute_command(self, command_type: str, action: str, parameters: Dict[str, Any] = None) -> CommandResult:
        """
        执行命令
        
        Args:
            command_type: 命令类型
            action: 操作类型
            parameters: 参数
            
        Returns:
            CommandResult: 执行结果
        """
        pass
    
    @abstractmethod
    async def get_system_info(self) -> SystemInfo:
        """
        获取系统信息
        
        Returns:
            SystemInfo: 系统信息
        """
        pass
    
    # 系统控制方法
    async def volume_up(self, amount: int = 10) -> CommandResult:
        """音量增加"""
        return await self.execute_command("system_control", "volume_up", {"amount": amount})
    
    async def volume_down(self, amount: int = 10) -> CommandResult:
        """音量减少"""
        return await self.execute_command("system_control", "volume_down", {"amount": amount})
    
    async def volume_set(self, volume: int) -> CommandResult:
        """设置音量"""
        return await self.execute_command("system_control", "volume_set", {"volume": volume})
    
    async def mute(self) -> CommandResult:
        """静音"""
        return await self.execute_command("system_control", "mute")
    
    async def unmute(self) -> CommandResult:
        """取消静音"""
        return await self.execute_command("system_control", "unmute")
    
    async def screenshot(self, save_path: str = None) -> CommandResult:
        """截图"""
        return await self.execute_command("system_control", "screenshot", {"save_path": save_path})
    
    async def lock_screen(self) -> CommandResult:
        """锁屏"""
        return await self.execute_command("system_control", "lock_screen")
    
    # 应用控制方法
    async def open_application(self, app_name: str, parameters: Dict[str, Any] = None) -> CommandResult:
        """打开应用程序"""
        return await self.execute_command("application", "open", {"app_name": app_name, "parameters": parameters})
    
    async def close_application(self, app_name: str) -> CommandResult:
        """关闭应用程序"""
        return await self.execute_command("application", "close", {"app_name": app_name})
    
    async def list_applications(self) -> CommandResult:
        """列出应用程序"""
        return await self.execute_command("application", "list")
    
    # 文件操作方法
    async def create_file(self, file_path: str, content: str = "") -> CommandResult:
        """创建文件"""
        return await self.execute_command("file_operation", "create_file", {"file_path": file_path, "content": content})
    
    async def read_file(self, file_path: str) -> CommandResult:
        """读取文件"""
        return await self.execute_command("file_operation", "read_file", {"file_path": file_path})
    
    async def write_file(self, file_path: str, content: str) -> CommandResult:
        """写入文件"""
        return await self.execute_command("file_operation", "write_file", {"file_path": file_path, "content": content})
    
    async def delete_file(self, file_path: str) -> CommandResult:
        """删除文件"""
        return await self.execute_command("file_operation", "delete_file", {"file_path": file_path})
    
    async def list_files(self, directory: str) -> CommandResult:
        """列出文件"""
        return await self.execute_command("file_operation", "list_files", {"directory": directory})
    
    # 媒体控制方法
    async def play_media(self, media_path: str) -> CommandResult:
        """播放媒体"""
        return await self.execute_command("media", "play", {"media_path": media_path})
    
    async def pause_media(self) -> CommandResult:
        """暂停媒体"""
        return await self.execute_command("media", "pause")
    
    async def stop_media(self) -> CommandResult:
        """停止媒体"""
        return await self.execute_command("media", "stop")
    
    # 查询方法
    async def get_time(self) -> CommandResult:
        """获取时间"""
        return await self.execute_command("query", "time")
    
    async def get_date(self) -> CommandResult:
        """获取日期"""
        return await self.execute_command("query", "date")
    
    async def get_weather(self, location: str = None) -> CommandResult:
        """获取天气"""
        return await self.execute_command("query", "weather", {"location": location})
    
    async def get_processes(self) -> CommandResult:
        """获取进程列表"""
        return await self.execute_command("query", "processes")
    
    def set_safety(self, enabled: bool) -> None:
        """设置安全模式"""
        self.safety_enabled = enabled
        logger.info(f"Safety mode {'enabled' if enabled else 'disabled'}")
    
    def set_command_delay(self, delay: float) -> None:
        """设置命令延迟"""
        self.command_delay = delay
        logger.info(f"Command delay set to {delay} seconds")

