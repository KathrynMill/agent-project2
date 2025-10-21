"""
Echo Command 主应用
"""
import asyncio
import json
import time
from typing import Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from config.settings import settings
from models.schemas import (
    WebSocketMessage, AudioMessage, TextMessage, CommandMessage, 
    ResponseMessage, ErrorMessage, HeartbeatMessage, SessionInfo
)
from services.session_manager import SessionManager
from services.command_executor import CommandExecutor
from services.ai.transcription_service import TranscriptionService
from services.ai.intent_parser_service import IntentParserService
from services.ai.tts_service import TTSService


# 创建FastAPI应用
app = FastAPI(
    title="Echo Command API",
    description="语音控制电脑应用的后端API",
    version=settings.app_version
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
session_manager = SessionManager()
command_executor = CommandExecutor()
transcription_service = TranscriptionService()
intent_parser_service = IntentParserService()
tts_service = TTSService()

# 活跃连接管理
active_connections: Dict[str, WebSocket] = {}


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"Echo Command API starting up on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("Echo Command API shutting down")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Echo Command API",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "active_connections": len(active_connections),
        "sessions": session_manager.get_session_stats()
    }


@app.get("/api/sessions")
async def get_sessions():
    """获取会话列表"""
    return {
        "sessions": [session.dict() for session in session_manager.get_active_sessions()],
        "stats": session_manager.get_session_stats()
    }


@app.post("/api/sessions")
async def create_session():
    """创建新会话"""
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """删除会话"""
    if session_manager.end_session(session_id):
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await websocket.accept()
    session_id = None
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理消息
            response = await handle_websocket_message(websocket, message_data)
            
            # 发送响应
            if response:
                await websocket.send_text(json.dumps(response.dict()))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # 清理连接
        if session_id and session_id in active_connections:
            del active_connections[session_id]
        if session_id:
            session_manager.end_session(session_id)


async def handle_websocket_message(websocket: WebSocket, message_data: Dict[str, Any]) -> WebSocketMessage:
    """处理WebSocket消息"""
    try:
        message_type = message_data.get("type")
        session_id = message_data.get("session_id")
        
        # 更新会话活动
        if session_id:
            session_manager.update_session_activity(session_id)
        
        if message_type == "audio":
            return await handle_audio_message(websocket, message_data)
        elif message_type == "text":
            return await handle_text_message(websocket, message_data)
        elif message_type == "command":
            return await handle_command_message(websocket, message_data)
        elif message_type == "heartbeat":
            return handle_heartbeat_message(message_data)
        else:
            return ErrorMessage(
                error_code="UNKNOWN_MESSAGE_TYPE",
                error_message=f"Unknown message type: {message_type}",
                session_id=session_id
            )
            
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        return ErrorMessage(
            error_code="MESSAGE_HANDLING_ERROR",
            error_message=str(e),
            session_id=message_data.get("session_id")
        )


async def handle_audio_message(websocket: WebSocket, message_data: Dict[str, Any]) -> WebSocketMessage:
    """处理音频消息"""
    try:
        session_id = message_data.get("session_id")
        
        # 创建会话（如果不存在）
        if not session_id:
            session_id = session_manager.create_session()
            active_connections[session_id] = websocket
        
        # 获取音频数据
        audio_data = message_data.get("audio_data", "").encode()
        sample_rate = message_data.get("sample_rate", 16000)
        
        # 语音识别
        transcription_result = await transcription_service.transcribe_audio(audio_data, sample_rate)
        
        if not transcription_result.text:
            return ResponseMessage(
                success=False,
                message="语音识别失败，请重试",
                session_id=session_id
            )
        
        # 意图解析
        intent_result = await intent_parser_service.parse_intent(transcription_result.text)
        
        # 执行命令
        command_result = await command_executor.execute_intent(intent_result, session_id)
        
        # 更新会话统计
        session_manager.increment_command_count(session_id)
        
        # 生成语音回复
        tts_result = await tts_service.text_to_speech(command_result.message)
        
        return ResponseMessage(
            success=command_result.success,
            message=command_result.message,
            data={
                "transcription": transcription_result.text,
                "intent": intent_result.intent,
                "execution_time": command_result.execution_time,
                "output": command_result.output
            },
            audio_response=tts_result.audio_data.hex() if tts_result.audio_data else None,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error handling audio message: {e}")
        return ErrorMessage(
            error_code="AUDIO_PROCESSING_ERROR",
            error_message=str(e),
            session_id=message_data.get("session_id")
        )


async def handle_text_message(websocket: WebSocket, message_data: Dict[str, Any]) -> WebSocketMessage:
    """处理文本消息"""
    try:
        session_id = message_data.get("session_id")
        text = message_data.get("text", "")
        
        if not text:
            return ErrorMessage(
                error_code="EMPTY_TEXT",
                error_message="文本内容为空",
                session_id=session_id
            )
        
        # 创建会话（如果不存在）
        if not session_id:
            session_id = session_manager.create_session()
            active_connections[session_id] = websocket
        
        # 意图解析
        intent_result = await intent_parser_service.parse_intent(text)
        
        # 执行命令
        command_result = await command_executor.execute_intent(intent_result, session_id)
        
        # 更新会话统计
        session_manager.increment_command_count(session_id)
        
        # 生成语音回复
        tts_result = await tts_service.text_to_speech(command_result.message)
        
        return ResponseMessage(
            success=command_result.success,
            message=command_result.message,
            data={
                "intent": intent_result.intent,
                "execution_time": command_result.execution_time,
                "output": command_result.output
            },
            audio_response=tts_result.audio_data.hex() if tts_result.audio_data else None,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error handling text message: {e}")
        return ErrorMessage(
            error_code="TEXT_PROCESSING_ERROR",
            error_message=str(e),
            session_id=message_data.get("session_id")
        )


async def handle_command_message(websocket: WebSocket, message_data: Dict[str, Any]) -> WebSocketMessage:
    """处理命令消息"""
    try:
        session_id = message_data.get("session_id")
        command_type = message_data.get("command_type")
        action = message_data.get("action")
        parameters = message_data.get("parameters", {})
        
        # 创建会话（如果不存在）
        if not session_id:
            session_id = session_manager.create_session()
            active_connections[session_id] = websocket
        
        # 直接执行命令
        from models.schemas import AIIntentResult, CommandType
        intent_result = AIIntentResult(
            intent="direct_command",
            confidence=1.0,
            entities=parameters,
            command_type=CommandType(command_type),
            action=action,
            parameters=parameters
        )
        
        command_result = await command_executor.execute_intent(intent_result, session_id)
        
        # 更新会话统计
        session_manager.increment_command_count(session_id)
        
        return ResponseMessage(
            success=command_result.success,
            message=command_result.message,
            data={
                "execution_time": command_result.execution_time,
                "output": command_result.output
            },
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error handling command message: {e}")
        return ErrorMessage(
            error_code="COMMAND_EXECUTION_ERROR",
            error_message=str(e),
            session_id=message_data.get("session_id")
        )


def handle_heartbeat_message(message_data: Dict[str, Any]) -> WebSocketMessage:
    """处理心跳消息"""
    session_id = message_data.get("session_id")
    
    if session_id:
        session_manager.update_session_activity(session_id)
    
    return HeartbeatMessage(session_id=session_id)


if __name__ == "__main__":
    import uvicorn
    
    # 配置日志
    logger.add(
        settings.log_file,
        rotation=settings.log_rotation,
        retention=settings.log_retention,
        level=settings.log_level
    )
    
    # 启动应用
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

