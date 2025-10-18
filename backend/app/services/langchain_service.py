"""
LangChain AI对话服务
"""
import json
from typing import AsyncGenerator, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.bazi_profile import BaziProfile


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
    
    def _build_system_prompt(self, bazi_info: Dict = None) -> str:
        """构建系统提示词"""
        base_prompt = """你是一位专业的命理分析师，精通八字命理。

请根据用户的问题进行专业分析。注意：
1. 分析要有理有据，引用命理术语
2. 语言要专业且易懂
3. 回答要有实用性建议
4. 保持命理文化的严肃性
"""
        
        if bazi_info:
            bazi_section = f"""
用户档案：
- 姓名：{bazi_info.get('name', '未知')}
- 性别：{bazi_info.get('gender', '未知')}
- 八字：{bazi_info.get('bazi', '未知')}
- 节气信息：{bazi_info.get('jieqi_info', '未知')}
- 大运信息：{bazi_info.get('dayun_info', '未知')}
"""
            return base_prompt + bazi_section
        
        return base_prompt
    
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
        # 获取会话信息
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        # 获取八字信息（如果有）
        bazi_info = None
        if conversation.bazi_profile_id:
            profile = db.query(BaziProfile).filter(
                BaziProfile.id == conversation.bazi_profile_id
            ).first()
            if profile:
                bazi_info = profile.bazi_result
        
        # 构建系统提示
        system_prompt = self._build_system_prompt(bazi_info)
        
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

