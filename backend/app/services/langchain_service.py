"""
LangChain AI对话服务
"""
import json
from typing import AsyncGenerator, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.bazi_profile import BaziProfile
from app.prompts import SystemPromptManager


class LangChainChatService:
    """LangChain聊天服务"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            streaming=True,
            openai_api_base=settings.OPENAI_BASE_URL,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def _build_system_prompt(
        self,
        ai_style: str = "professional",
        bazi_info: Optional[Dict] = None
    ) -> str:
        """
        构建系统提示词
        
        Args:
            ai_style: AI对话风格 (simple/balanced/professional)
            bazi_info: 八字档案信息（包含name, gender和bazi_result中的数据）
            
        Returns:
            完整的系统提示词
        """
        return SystemPromptManager.build_system_prompt(
            ai_style=ai_style,
            bazi_info=bazi_info
        )
    
    def _load_context_messages(
        self,
        conversation_id: str,
        context_size: int,
        db: Session
    ) -> list:
        """加载上下文消息"""
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(context_size).all()
        
        # 转换为LangChain消息格式
        context = []
        for msg in reversed(messages):
            if msg.role == "user":
                context.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                context.append(AIMessage(content=msg.content))
        
        return context
    
    async def stream_chat(
        self,
        user_message: str,
        conversation_id: str,
        user_id: str,
        db: Session
    ) -> AsyncGenerator[Dict, None]:
        """
        流式对话
        
        Args:
            user_message: 用户消息
            conversation_id: 会话ID
            user_id: 用户ID
            db: 数据库会话
            
        Yields:
            消息块字典
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # 获取会话信息
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        logger.info(f"📌 会话ID: {conversation_id}")
        logger.info(f"🎨 对话模式: {conversation.ai_style}")
        logger.info(f"📊 上下文条数: {conversation.context_size}")
        logger.info(f"🔗 关联八字档案ID: {conversation.bazi_profile_id}")
        
        # 获取AI对话风格
        ai_style = conversation.ai_style or "professional"
        
        # 获取八字信息（如果有）
        bazi_info = None
        if conversation.bazi_profile_id:
            logger.info(f"🔍 正在查询八字档案: {conversation.bazi_profile_id}")
            profile = db.query(BaziProfile).filter(
                BaziProfile.id == conversation.bazi_profile_id
            ).first()
            
            if profile:
                # 组合八字档案的完整信息
                bazi_info = {
                    'name': profile.name,
                    'gender': profile.gender,
                    # 从bazi_result字段获取八字分析数据
                    **(profile.bazi_result or {})
                }
                logger.info(f"✅ 八字档案加载成功: {profile.name} ({profile.gender})")
                logger.info(f"   八字字段: {list(profile.bazi_result.keys()) if profile.bazi_result else '无'}")
            else:
                logger.warning(f"⚠️ 未找到八字档案: {conversation.bazi_profile_id}")
        else:
            logger.info("ℹ️ 当前会话未关联八字档案")
        
        # 构建系统提示（传入ai_style和完整的bazi_info）
        system_prompt = self._build_system_prompt(
            ai_style=ai_style,
            bazi_info=bazi_info
        )
        
        # 加载上下文
        context_messages = self._load_context_messages(
            conversation_id,
            conversation.context_size,
            db
        )
        
        # 构建完整消息列表
        messages = [SystemMessage(content=system_prompt)]
        messages.extend(context_messages)
        messages.append(HumanMessage(content=user_message))
        
        # 流式生成响应
        full_response = ""
        token_count = 0
        
        try:
            async for chunk in self.llm.astream(messages):
                content = chunk.content
                if content:
                    full_response += content
                    token_count += 1
                    
                    yield {
                        "type": "token",
                        "content": content,
                        "token_cost": token_count
                    }
        
        except Exception as e:
            yield {
                "type": "error",
                "message": f"AI对话失败：{str(e)}"
            }

