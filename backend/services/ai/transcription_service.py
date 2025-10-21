"""
语音识别服务
"""
import asyncio
import io
import tempfile
import os
from typing import Optional
import whisper
import numpy as np
from loguru import logger

from models.schemas import AITranscriptionResult


class TranscriptionService:
    """语音识别服务类"""
    
    def __init__(self, model_size: str = "base"):
        """
        初始化语音识别服务
        
        Args:
            model_size: Whisper模型大小 (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载Whisper模型"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    async def transcribe_audio(self, audio_data: bytes, sample_rate: int = 16000) -> AITranscriptionResult:
        """
        将音频数据转换为文本
        
        Args:
            audio_data: 音频字节数据
            sample_rate: 采样率
            
        Returns:
            AITranscriptionResult: 转录结果
        """
        try:
            # 将字节数据转换为numpy数组
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # 如果采样率不是16000，需要重采样
            if sample_rate != 16000:
                try:
                    import librosa
                    audio_array = librosa.resample(audio_array, orig_sr=sample_rate, target_sr=16000)
                except ImportError:
                    # 如果没有librosa，使用简单的线性插值
                    import scipy.signal
                    new_length = int(len(audio_array) * 16000 / sample_rate)
                    audio_array = scipy.signal.resample(audio_array, new_length)
            
            # 使用临时文件进行转录
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                # 保存音频数据到临时文件
                try:
                    import soundfile as sf
                    sf.write(temp_file.name, audio_array, 16000)
                except ImportError:
                    # 如果没有soundfile，使用wave模块
                    import wave
                    with wave.open(temp_file.name, 'wb') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)
                        wav_file.setframerate(16000)
                        wav_file.writeframes((audio_array * 32767).astype(np.int16).tobytes())
                
                # 执行转录
                result = await asyncio.get_event_loop().run_in_executor(
                    None, self._transcribe_file, temp_file.name
                )
                
                # 清理临时文件
                os.unlink(temp_file.name)
                
                return result
                
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return AITranscriptionResult(
                text="",
                confidence=0.0,
                language="zh-CN",
                duration=0.0
            )
    
    def _transcribe_file(self, file_path: str) -> AITranscriptionResult:
        """
        转录音频文件
        
        Args:
            file_path: 音频文件路径
            
        Returns:
            AITranscriptionResult: 转录结果
        """
        try:
            result = self.model.transcribe(file_path, language="zh")
            
            return AITranscriptionResult(
                text=result["text"].strip(),
                confidence=0.9,  # Whisper不直接提供置信度，使用固定值
                language=result.get("language", "zh-CN"),
                duration=len(result["text"]) * 0.1  # 估算持续时间
            )
        except Exception as e:
            logger.error(f"File transcription failed: {e}")
            return AITranscriptionResult(
                text="",
                confidence=0.0,
                language="zh-CN",
                duration=0.0
            )
    
    async def transcribe_stream(self, audio_stream: bytes) -> AITranscriptionResult:
        """
        流式转录音频数据
        
        Args:
            audio_stream: 音频流数据
            
        Returns:
            AITranscriptionResult: 转录结果
        """
        # 对于流式转录，这里简化处理
        # 实际应用中可能需要更复杂的缓冲和分段处理
        return await self.transcribe_audio(audio_stream)
    
    def get_supported_languages(self) -> list:
        """获取支持的语言列表"""
        return ["zh-CN", "en-US", "ja-JP", "ko-KR"]
    
    def set_language(self, language: str):
        """设置识别语言"""
        # Whisper支持的语言设置
        supported_langs = {
            "zh-CN": "zh",
            "en-US": "en",
            "ja-JP": "ja",
            "ko-KR": "ko"
        }
        return supported_langs.get(language, "zh")
