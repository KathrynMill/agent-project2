"""
数据模型定义
"""
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """消息类型枚举"""
    AUDIO = "audio"
    TEXT = "text"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class CommandType(str, Enum):
    """命令类型枚举"""
    SYSTEM_CONTROL = "system_control"
    FILE_OPERATION = "file_operation"
    TEXT_PROCESSING = "text_processing"
    APPLICATION = "application"
    MEDIA = "media"
    QUERY = "query"


class SystemAction(str, Enum):
    """系统操作枚举"""
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    VOLUME_SET = "volume_set"
    MUTE = "mute"
    UNMUTE = "unmute"
    SCREENSHOT = "screenshot"
    LOCK_SCREEN = "lock_screen"
    SHUTDOWN = "shutdown"
    RESTART = "restart"


class FileAction(str, Enum):
    """文件操作枚举"""
    CREATE_FILE = "create_file"
    READ_FILE = "read_file"
    WRITE_FILE = "write_file"
    DELETE_FILE = "delete_file"
    LIST_FILES = "list_files"
    SEARCH_FILES = "search_files"


class TextAction(str, Enum):
    """文本处理枚举"""
    WRITE_ARTICLE = "write_article"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    CORRECT_GRAMMAR = "correct_grammar"
    EXTRACT_KEYWORDS = "extract_keywords"


class WebSocketMessage(BaseModel):
    """WebSocket消息基类"""
    type: MessageType
    timestamp: float = Field(default_factory=lambda: __import__('time').time())
    session_id: Optional[str] = None


class AudioMessage(WebSocketMessage):
    """音频消息"""
    type: MessageType = MessageType.AUDIO
    audio_data: bytes
    sample_rate: int = 16000
    channels: int = 1


class TextMessage(WebSocketMessage):
    """文本消息"""
    type: MessageType = MessageType.TEXT
    text: str
    language: str = "zh-CN"


class CommandMessage(WebSocketMessage):
    """命令消息"""
    type: MessageType = MessageType.COMMAND
    command_type: CommandType
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    target: Optional[str] = None


class ResponseMessage(WebSocketMessage):
    """响应消息"""
    type: MessageType = MessageType.RESPONSE
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    audio_response: Optional[bytes] = None


class ErrorMessage(WebSocketMessage):
    """错误消息"""
    type: MessageType = MessageType.ERROR
    error_code: str
    error_message: str
    details: Optional[Dict[str, Any]] = None


class HeartbeatMessage(WebSocketMessage):
    """心跳消息"""
    type: MessageType = MessageType.HEARTBEAT
    status: str = "alive"


class SessionInfo(BaseModel):
    """会话信息"""
    session_id: str
    user_id: Optional[str] = None
    start_time: float
    last_activity: float
    is_active: bool = True
    commands_count: int = 0


class SystemInfo(BaseModel):
    """系统信息"""
    os_name: str
    os_version: str
    cpu_count: int
    memory_total: int
    memory_available: int
    disk_usage: Dict[str, Any]


class CommandResult(BaseModel):
    """命令执行结果"""
    success: bool
    message: str
    execution_time: float
    output: Optional[str] = None
    error: Optional[str] = None


class AITranscriptionResult(BaseModel):
    """AI转录结果"""
    text: str
    confidence: float
    language: str
    duration: float


class AIIntentResult(BaseModel):
    """AI意图解析结果"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    command_type: CommandType
    action: str
    parameters: Dict[str, Any]


class TTSResult(BaseModel):
    """TTS结果"""
    audio_data: bytes
    duration: float
    sample_rate: int = 22050
    text: str

