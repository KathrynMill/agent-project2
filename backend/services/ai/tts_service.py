"""
文本转语音服务
"""
import asyncio
import io
import tempfile
from typing import Optional
import pyttsx3
import pygame
from loguru import logger

from models.schemas import TTSResult
from config.settings import settings


class TTSService:
    """文本转语音服务类"""
    
    def __init__(self):
        """初始化TTS服务"""
        self.engine = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """初始化TTS引擎"""
        try:
            self.engine = pyttsx3.init()
            
            # 设置语音参数
            self.engine.setProperty('rate', settings.tts_rate)
            self.engine.setProperty('volume', settings.tts_volume)
            
            # 设置语音
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > settings.tts_voice_id:
                self.engine.setProperty('voice', voices[settings.tts_voice_id].id)
            
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            raise
    
    async def text_to_speech(self, text: str, language: str = "zh-CN") -> TTSResult:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            language: 语言代码
            
        Returns:
            TTSResult: TTS结果
        """
        try:
            # 使用临时文件保存音频
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # 异步执行TTS
            audio_data = await asyncio.get_event_loop().run_in_executor(
                None, self._synthesize_speech, text, temp_path
            )
            
            # 清理临时文件
            import os
            os.unlink(temp_path)
            
            return TTSResult(
                audio_data=audio_data,
                duration=len(audio_data) / (settings.tts_rate * 2),  # 估算持续时间
                sample_rate=22050,
                text=text
            )
            
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return TTSResult(
                audio_data=b"",
                duration=0.0,
                sample_rate=22050,
                text=text
            )
    
    def _synthesize_speech(self, text: str, output_path: str) -> bytes:
        """
        合成语音并保存到文件
        
        Args:
            text: 要转换的文本
            output_path: 输出文件路径
            
        Returns:
            bytes: 音频数据
        """
        try:
            # 保存到临时文件
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            # 读取音频数据
            with open(output_path, 'rb') as f:
                audio_data = f.read()
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            return b""
    
    async def speak_async(self, text: str) -> None:
        """
        异步播放语音
        
        Args:
            text: 要播放的文本
        """
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, self._speak_sync, text
            )
        except Exception as e:
            logger.error(f"Async speech failed: {e}")
    
    def _speak_sync(self, text: str) -> None:
        """
        同步播放语音
        
        Args:
            text: 要播放的文本
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Sync speech failed: {e}")
    
    def get_available_voices(self) -> list:
        """获取可用的语音列表"""
        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    "id": voice.id,
                    "name": voice.name,
                    "languages": getattr(voice, 'languages', [])
                }
                for voice in voices
            ]
        except Exception as e:
            logger.error(f"Failed to get voices: {e}")
            return []
    
    def set_voice(self, voice_id: int) -> bool:
        """
        设置语音
        
        Args:
            voice_id: 语音ID
            
        Returns:
            bool: 是否设置成功
        """
        try:
            voices = self.engine.getProperty('voices')
            if voices and 0 <= voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to set voice: {e}")
            return False
    
    def set_rate(self, rate: int) -> None:
        """
        设置语速
        
        Args:
            rate: 语速（每分钟字数）
        """
        try:
            self.engine.setProperty('rate', rate)
        except Exception as e:
            logger.error(f"Failed to set rate: {e}")
    
    def set_volume(self, volume: float) -> None:
        """
        设置音量
        
        Args:
            volume: 音量（0.0-1.0）
        """
        try:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
    
    def stop(self) -> None:
        """停止当前播放"""
        try:
            self.engine.stop()
        except Exception as e:
            logger.error(f"Failed to stop TTS: {e}")
    
    def is_speaking(self) -> bool:
        """检查是否正在播放"""
        try:
            return self.engine.isBusy()
        except Exception as e:
            logger.error(f"Failed to check speaking status: {e}")
            return False

