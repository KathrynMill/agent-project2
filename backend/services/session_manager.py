"""
会话管理器
"""
import asyncio
import time
import uuid
from typing import Dict, Optional, List
from loguru import logger

from models.schemas import SessionInfo, WebSocketMessage, MessageType


class SessionManager:
    """会话管理器类"""
    
    def __init__(self):
        """初始化会话管理器"""
        self.sessions: Dict[str, SessionInfo] = {}
        self.max_sessions = 100
        self.session_timeout = 3600  # 1小时超时
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """
        创建新会话
        
        Args:
            user_id: 用户ID（可选）
            
        Returns:
            str: 会话ID
        """
        session_id = str(uuid.uuid4())
        current_time = time.time()
        
        session_info = SessionInfo(
            session_id=session_id,
            user_id=user_id,
            start_time=current_time,
            last_activity=current_time,
            is_active=True,
            commands_count=0
        )
        
        self.sessions[session_id] = session_info
        
        # 清理过期会话
        asyncio.create_task(self._cleanup_expired_sessions())
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """
        获取会话信息
        
        Args:
            session_id: 会话ID
            
        Returns:
            Optional[SessionInfo]: 会话信息
        """
        return self.sessions.get(session_id)
    
    def update_session_activity(self, session_id: str) -> bool:
        """
        更新会话活动时间
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 是否更新成功
        """
        session = self.sessions.get(session_id)
        if session:
            session.last_activity = time.time()
            return True
        return False
    
    def increment_command_count(self, session_id: str) -> bool:
        """
        增加命令计数
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 是否更新成功
        """
        session = self.sessions.get(session_id)
        if session:
            session.commands_count += 1
            session.last_activity = time.time()
            return True
        return False
    
    def end_session(self, session_id: str) -> bool:
        """
        结束会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 是否结束成功
        """
        session = self.sessions.get(session_id)
        if session:
            session.is_active = False
            logger.info(f"Session ended: {session_id}, commands executed: {session.commands_count}")
            return True
        return False
    
    def get_active_sessions(self) -> List[SessionInfo]:
        """
        获取所有活跃会话
        
        Returns:
            List[SessionInfo]: 活跃会话列表
        """
        return [session for session in self.sessions.values() if session.is_active]
    
    def get_session_stats(self) -> Dict[str, any]:
        """
        获取会话统计信息
        
        Returns:
            Dict[str, any]: 统计信息
        """
        active_sessions = self.get_active_sessions()
        total_commands = sum(session.commands_count for session in self.sessions.values())
        
        return {
            "total_sessions": len(self.sessions),
            "active_sessions": len(active_sessions),
            "total_commands": total_commands,
            "average_commands_per_session": total_commands / len(self.sessions) if self.sessions else 0
        }
    
    async def _cleanup_expired_sessions(self):
        """清理过期会话"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session.last_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.end_session(session_id)
            logger.info(f"Cleaned up expired session: {session_id}")
    
    def validate_session(self, session_id: str) -> bool:
        """
        验证会话是否有效
        
        Args:
            session_id: 会话ID
            
        Returns:
            bool: 会话是否有效
        """
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        if not session.is_active:
            return False
        
        # 检查是否超时
        if time.time() - session.last_activity > self.session_timeout:
            self.end_session(session_id)
            return False
        
        return True
    
    def get_user_sessions(self, user_id: str) -> List[SessionInfo]:
        """
        获取用户的所有会话
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[SessionInfo]: 用户会话列表
        """
        return [session for session in self.sessions.values() if session.user_id == user_id]
    
    def cleanup_user_sessions(self, user_id: str) -> int:
        """
        清理用户的所有会话
        
        Args:
            user_id: 用户ID
            
        Returns:
            int: 清理的会话数量
        """
        user_sessions = self.get_user_sessions(user_id)
        count = 0
        
        for session in user_sessions:
            if self.end_session(session.session_id):
                count += 1
        
        logger.info(f"Cleaned up {count} sessions for user: {user_id}")
        return count



