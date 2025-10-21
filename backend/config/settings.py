"""
应用配置管理模块
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    app_name: str = Field(default="EchoCommand", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    host: str = Field(default="127.0.0.1", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # OpenAI配置
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    
    # WebSocket配置
    ws_max_connections: int = Field(default=100, env="WS_MAX_CONNECTIONS")
    ws_heartbeat_interval: int = Field(default=30, env="WS_HEARTBEAT_INTERVAL")
    
    # 音频配置
    audio_sample_rate: int = Field(default=16000, env="AUDIO_SAMPLE_RATE")
    audio_chunk_size: int = Field(default=1024, env="AUDIO_CHUNK_SIZE")
    audio_channels: int = Field(default=1, env="AUDIO_CHANNELS")
    
    # TTS配置
    tts_rate: int = Field(default=200, env="TTS_RATE")
    tts_volume: float = Field(default=0.9, env="TTS_VOLUME")
    tts_voice_id: int = Field(default=0, env="TTS_VOICE_ID")
    
    # 系统控制配置
    auto_safety: bool = Field(default=True, env="AUTO_SAFETY")
    command_delay: float = Field(default=0.1, env="COMMAND_DELAY")
    scroll_amount: int = Field(default=3, env="SCROLL_AMOUNT")
    
    # 日志配置
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/echo_command.log", env="LOG_FILE")
    log_rotation: str = Field(default="1 day", env="LOG_ROTATION")
    log_retention: str = Field(default="7 days", env="LOG_RETENTION")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings

