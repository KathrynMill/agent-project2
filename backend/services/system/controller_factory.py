"""
系统控制器工厂
"""
import platform
from typing import Type
from loguru import logger

from .base_controller import BaseController
from .windows_controller import WindowsController
from .linux_controller import LinuxController
from .macos_controller import MacOSController


class ControllerFactory:
    """系统控制器工厂类"""
    
    @staticmethod
    def create_controller() -> BaseController:
        """
        根据当前操作系统创建相应的控制器
        
        Returns:
            BaseController: 系统控制器实例
        """
        system = platform.system().lower()
        
        try:
            if system == "windows":
                logger.info("Creating Windows controller")
                return WindowsController()
            elif system == "linux":
                logger.info("Creating Linux controller")
                return LinuxController()
            elif system == "darwin":
                logger.info("Creating macOS controller")
                return MacOSController()
            else:
                logger.warning(f"Unsupported operating system: {system}, using Linux controller as fallback")
                return LinuxController()
                
        except Exception as e:
            logger.error(f"Failed to create controller for {system}: {e}")
            # 返回基础控制器作为后备
            return BaseController()
    
    @staticmethod
    def get_supported_systems() -> list:
        """获取支持的操作系统列表"""
        return ["windows", "linux", "darwin"]
    
    @staticmethod
    def get_current_system() -> str:
        """获取当前操作系统"""
        return platform.system().lower()

