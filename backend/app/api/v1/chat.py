"""
对话相关API
"""
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.api.deps import get_current_user, check_token_balance
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    ChatHistoryResponse
)
from app.services.langchain_service import LangChainChatService

router = APIRouter()
chat_service = LangChainChatService()


@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新会话"""
    conversation = Conversation(
        user_id=current_user.id,
        **conversation_data.model_dump()
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取会话列表"""
    conversations = db.query(Conversation).filter(
        and_(
            Conversation.user_id == current_user.id,
            Conversation.deleted_at.is_(None)
        )
    ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()
    
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取会话详情"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id,
        Conversation.deleted_at.is_(None)
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    return conversation


@router.put("/conversations/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: str,
    update_data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新会话"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(conversation, field, value)
    
    db.commit()
    db.refresh(conversation)
    
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除会话（软删除）"""
    from datetime import datetime
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    conversation.deleted_at = datetime.utcnow()
    db.commit()
    
    return {"message": "删除成功"}


@router.post("/message")
async def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_token_balance)
):
    """
    发送消息（流式响应）
    """
    # 检查用户是否有八字档案
    from app.models.bazi_profile import BaziProfile
    bazi_count = db.query(BaziProfile).filter(
        BaziProfile.user_id == current_user.id
    ).count()
    
    if bazi_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先设置出生信息才能使用AI对话功能"
        )
    
    # 验证会话
    conversation = db.query(Conversation).filter(
        Conversation.id == message_data.conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    # 保存用户消息
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()
    
    # 在外部保存ID，避免session问题
    conversation_id = str(conversation.id)
    user_id = str(current_user.id)
    
    # 流式生成AI响应
    async def generate():
        from app.core.database import SessionLocal
        
        # 创建新的db session用于流式响应
        stream_db = SessionLocal()
        
        try:
            full_response = ""
            token_cost = 0
            
            async for chunk in chat_service.stream_chat(
                user_message=message_data.content,
                conversation_id=conversation_id,
                user_id=user_id,
                db=stream_db
            ):
                if chunk.get("type") == "token":
                    full_response += chunk.get("content", "")
                    token_cost = chunk.get("token_cost", 0)
                
                # 使用json.dumps确保正确的JSON格式
                yield f"data: {json.dumps(chunk)}\n\n"
            
            # 保存AI响应
            ai_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=full_response,
                token_cost=token_cost
            )
            stream_db.add(ai_message)
            
            # 扣减用户token
            user = stream_db.query(User).filter(User.id == user_id).first()
            if user:
                user.token_balance -= token_cost
            
            stream_db.commit()
            stream_db.refresh(ai_message)
            
            # 发送完成消息
            done_data = {
                "type": "done",
                "message_id": str(ai_message.id),
                "token_cost": token_cost
            }
            yield f"data: {json.dumps(done_data)}\n\n"
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"流式对话错误: {error_detail}")
            
            error_data = {
                "type": "error",
                "message": str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
        
        finally:
            stream_db.close()
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history/{conversation_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    conversation_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取会话历史"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    total = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).count()
    
    return ChatHistoryResponse(
        conversation=conversation,
        messages=list(reversed(messages)),
        total=total
    )

