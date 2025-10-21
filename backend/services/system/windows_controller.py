"""
Windows系统控制器
"""
import asyncio
import subprocess
import os
import time
import psutil
import pyautogui
from typing import Dict, Any
from loguru import logger

from .base_controller import BaseController
from models.schemas import CommandResult, SystemInfo


class WindowsController(BaseController):
    """Windows系统控制器"""
    
    def __init__(self):
        """初始化Windows控制器"""
        super().__init__()
        self._setup_audio_control()
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def _setup_audio_control(self):
        """设置音频控制"""
        try:
            # 检查是否有nircmd
            result = subprocess.run(['where', 'nircmd'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.audio_control = 'nircmd'
            else:
                # 使用PowerShell
                self.audio_control = 'powershell'
            logger.info(f"Audio control method: {self.audio_control}")
        except Exception as e:
            logger.error(f"Failed to setup audio control: {e}")
            self.audio_control = 'powershell'
    
    async def execute_command(self, command_type: str, action: str, parameters: Dict[str, Any] = None) -> CommandResult:
        """执行命令"""
        start_time = time.time()
        
        try:
            if command_type == "system_control":
                return await self._handle_system_control(action, parameters or {})
            elif command_type == "application":
                return await self._handle_application_control(action, parameters or {})
            elif command_type == "file_operation":
                return await self._handle_file_operation(action, parameters or {})
            elif command_type == "media":
                return await self._handle_media_control(action, parameters or {})
            elif command_type == "query":
                return await self._handle_query(action, parameters or {})
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown command type: {command_type}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return CommandResult(
                success=False,
                message=f"Command execution failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _handle_system_control(self, action: str, parameters: Dict[str, Any]) -> CommandResult:
        """处理系统控制命令"""
        start_time = time.time()
        
        try:
            if action == "volume_up":
                amount = parameters.get("amount", 10)
                return await self._volume_up(amount)
            elif action == "volume_down":
                amount = parameters.get("amount", 10)
                return await self._volume_down(amount)
            elif action == "volume_set":
                volume = parameters.get("volume", 50)
                return await self._volume_set(volume)
            elif action == "mute":
                return await self._mute()
            elif action == "unmute":
                return await self._unmute()
            elif action == "screenshot":
                save_path = parameters.get("save_path")
                return await self._screenshot(save_path)
            elif action == "lock_screen":
                return await self._lock_screen()
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown system control action: {action}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"System control failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _volume_up(self, amount: int) -> CommandResult:
        """音量增加"""
        start_time = time.time()
        
        try:
            if self.audio_control == 'nircmd':
                cmd = ['nircmd', 'changesysvolume', str(amount * 655)]
            else:
                # 使用PowerShell
                cmd = [
                    'powershell', '-Command',
                    f'(New-Object -ComObject WScript.Shell).SendKeys([char]175)'
                ]
            
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message=f"Volume increased by {amount}%",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Failed to increase volume: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Volume up failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _volume_down(self, amount: int) -> CommandResult:
        """音量减少"""
        start_time = time.time()
        
        try:
            if self.audio_control == 'nircmd':
                cmd = ['nircmd', 'changesysvolume', str(-amount * 655)]
            else:
                # 使用PowerShell
                cmd = [
                    'powershell', '-Command',
                    f'(New-Object -ComObject WScript.Shell).SendKeys([char]174)'
                ]
            
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message=f"Volume decreased by {amount}%",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Failed to decrease volume: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Volume down failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _volume_set(self, volume: int) -> CommandResult:
        """设置音量"""
        start_time = time.time()
        
        try:
            if self.audio_control == 'nircmd':
                cmd = ['nircmd', 'setsysvolume', str(int(volume * 655.35))]
            else:
                # 使用PowerShell
                cmd = [
                    'powershell', '-Command',
                    f'[audio]::Volume = {volume / 100.0}'
                ]
            
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message=f"Volume set to {volume}%",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Failed to set volume: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Volume set failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _mute(self) -> CommandResult:
        """静音"""
        start_time = time.time()
        
        try:
            if self.audio_control == 'nircmd':
                cmd = ['nircmd', 'mutesysvolume', '1']
            else:
                # 使用PowerShell
                cmd = [
                    'powershell', '-Command',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
                ]
            
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message="Audio muted",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Failed to mute: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Mute failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _unmute(self) -> CommandResult:
        """取消静音"""
        start_time = time.time()
        
        try:
            if self.audio_control == 'nircmd':
                cmd = ['nircmd', 'mutesysvolume', '0']
            else:
                # 使用PowerShell
                cmd = [
                    'powershell', '-Command',
                    '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'
                ]
            
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message="Audio unmuted",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Failed to unmute: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Unmute failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _screenshot(self, save_path: str = None) -> CommandResult:
        """截图"""
        start_time = time.time()
        
        try:
            if not save_path:
                save_path = f"C:\\temp\\screenshot_{int(time.time())}.png"
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 使用pyautogui截图
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            
            return CommandResult(
                success=True,
                message=f"Screenshot saved to {save_path}",
                execution_time=time.time() - start_time,
                output=save_path
            )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Screenshot failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _lock_screen(self) -> CommandResult:
        """锁屏"""
        start_time = time.time()
        
        try:
            # 使用rundll32命令锁屏
            cmd = ['rundll32.exe', 'user32.dll,LockWorkStation']
            result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                return CommandResult(
                    success=True,
                    message="Screen locked",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Lock screen failed: {stderr.decode()}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Lock screen failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _handle_application_control(self, action: str, parameters: Dict[str, Any]) -> CommandResult:
        """处理应用控制命令"""
        start_time = time.time()
        
        try:
            if action == "open":
                app_name = parameters.get("app_name")
                if not app_name:
                    return CommandResult(
                        success=False,
                        message="Application name not provided",
                        execution_time=time.time() - start_time
                    )
                
                # 尝试直接启动应用
                cmd = ['start', app_name]
                result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                stdout, stderr = await result.communicate()
                
                if result.returncode == 0:
                    return CommandResult(
                        success=True,
                        message=f"Application {app_name} opened",
                        execution_time=time.time() - start_time
                    )
                else:
                    return CommandResult(
                        success=False,
                        message=f"Failed to open application: {stderr.decode()}",
                        execution_time=time.time() - start_time
                    )
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown application action: {action}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Application control failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _handle_file_operation(self, action: str, parameters: Dict[str, Any]) -> CommandResult:
        """处理文件操作命令"""
        start_time = time.time()
        
        try:
            if action == "create_file":
                file_path = parameters.get("file_path")
                content = parameters.get("content", "")
                
                if not file_path:
                    return CommandResult(
                        success=False,
                        message="File path not provided",
                        execution_time=time.time() - start_time
                    )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return CommandResult(
                    success=True,
                    message=f"File {file_path} created",
                    execution_time=time.time() - start_time
                )
            
            elif action == "read_file":
                file_path = parameters.get("file_path")
                
                if not file_path:
                    return CommandResult(
                        success=False,
                        message="File path not provided",
                        execution_time=time.time() - start_time
                    )
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return CommandResult(
                    success=True,
                    message=f"File {file_path} read successfully",
                    execution_time=time.time() - start_time,
                    output=content
                )
            
            elif action == "write_file":
                file_path = parameters.get("file_path")
                content = parameters.get("content", "")
                
                if not file_path:
                    return CommandResult(
                        success=False,
                        message="File path not provided",
                        execution_time=time.time() - start_time
                    )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                return CommandResult(
                    success=True,
                    message=f"File {file_path} written successfully",
                    execution_time=time.time() - start_time
                )
            
            elif action == "delete_file":
                file_path = parameters.get("file_path")
                
                if not file_path:
                    return CommandResult(
                        success=False,
                        message="File path not provided",
                        execution_time=time.time() - start_time
                    )
                
                os.remove(file_path)
                
                return CommandResult(
                    success=True,
                    message=f"File {file_path} deleted",
                    execution_time=time.time() - start_time
                )
            
            elif action == "list_files":
                directory = parameters.get("directory", ".")
                
                files = os.listdir(directory)
                
                return CommandResult(
                    success=True,
                    message=f"Files in {directory} listed",
                    execution_time=time.time() - start_time,
                    output="\n".join(files)
                )
            
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown file operation: {action}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"File operation failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _handle_media_control(self, action: str, parameters: Dict[str, Any]) -> CommandResult:
        """处理媒体控制命令"""
        start_time = time.time()
        
        try:
            if action == "play":
                media_path = parameters.get("media_path")
                
                if not media_path:
                    return CommandResult(
                        success=False,
                        message="Media path not provided",
                        execution_time=time.time() - start_time
                    )
                
                # 使用Windows Media Player播放
                cmd = ['wmplayer', media_path]
                result = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                return CommandResult(
                    success=True,
                    message=f"Playing media: {media_path}",
                    execution_time=time.time() - start_time
                )
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown media action: {action}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Media control failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def _handle_query(self, action: str, parameters: Dict[str, Any]) -> CommandResult:
        """处理查询命令"""
        start_time = time.time()
        
        try:
            if action == "time":
                import datetime
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                return CommandResult(
                    success=True,
                    message=f"Current time: {current_time}",
                    execution_time=time.time() - start_time,
                    output=current_time
                )
            
            elif action == "date":
                import datetime
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                return CommandResult(
                    success=True,
                    message=f"Current date: {current_date}",
                    execution_time=time.time() - start_time,
                    output=current_date
                )
            
            elif action == "processes":
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        processes.append(proc.info)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                return CommandResult(
                    success=True,
                    message="Process list retrieved",
                    execution_time=time.time() - start_time,
                    output=str(processes)
                )
            
            else:
                return CommandResult(
                    success=False,
                    message=f"Unknown query action: {action}",
                    execution_time=time.time() - start_time
                )
        except Exception as e:
            return CommandResult(
                success=False,
                message=f"Query failed: {str(e)}",
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def get_system_info(self) -> SystemInfo:
        """获取系统信息"""
        try:
            return SystemInfo(
                os_name="Windows",
                os_version=os.uname().release if hasattr(os, 'uname') else "Unknown",
                cpu_count=psutil.cpu_count(),
                memory_total=psutil.virtual_memory().total,
                memory_available=psutil.virtual_memory().available,
                disk_usage=dict(psutil.disk_usage('C:\\')._asdict())
            )
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return SystemInfo(
                os_name="Windows",
                os_version="Unknown",
                cpu_count=0,
                memory_total=0,
                memory_available=0,
                disk_usage={}
            )



