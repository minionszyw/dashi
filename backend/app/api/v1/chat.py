from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing import List
from decimal import Decimal
from app.core.database import get_db
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse
)
from app.schemas.common import ResponseModel
from app.api.dependencies import get_current_user
from app.services.ai import ai_service
from app.services.billing import billing_service
import json

router = APIRouter()


@router.post("/sessions", response_model=ResponseModel)
async def create_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建会话"""
    session = ChatSession(
        user_id=current_user.id,
        title=session_data.title,
        status="active"
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return ResponseModel(
        data=ChatSessionResponse.model_validate(session)
    )


@router.get("/sessions", response_model=ResponseModel)
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话列表"""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .where(ChatSession.status != "deleted")
        .order_by(ChatSession.updated_at.desc())
    )
    sessions = result.scalars().all()
    
    return ResponseModel(
        data=[ChatSessionResponse.model_validate(s) for s in sessions]
    )


@router.get("/sessions/{session_id}", response_model=ResponseModel)
async def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取会话详情"""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 获取消息历史
    msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    messages = msg_result.scalars().all()
    
    return ResponseModel(
        data=ChatHistoryResponse(
            session=ChatSessionResponse.model_validate(session),
            messages=[ChatMessageResponse.model_validate(m) for m in messages]
        )
    )


@router.delete("/sessions/{session_id}", response_model=ResponseModel)
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除会话"""
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 软删除
    await db.execute(
        update(ChatSession)
        .where(ChatSession.id == session_id)
        .values(status="deleted")
    )
    await db.commit()
    
    return ResponseModel(message="删除成功")


@router.post("/messages", response_model=ResponseModel)
async def send_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送消息（非流式）"""
    # 验证会话
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == message_data.session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 获取历史消息
    msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == message_data.session_id)
        .order_by(ChatMessage.created_at)
    )
    history_msgs = msg_result.scalars().all()
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_msgs
    ]
    
    # 保存用户消息
    user_message = ChatMessage(
        session_id=message_data.session_id,
        role="user",
        content=message_data.content,
        tokens_used=0
    )
    db.add(user_message)
    
    # 获取AI回复
    ai_content, tokens_used = await ai_service.get_response(
        message_data.content,
        history
    )
    
    # 检查余额
    if not await billing_service.check_balance(db, current_user.id, Decimal(tokens_used * 0.001)):
        raise HTTPException(status_code=402, detail="余额不足")
    
    # 扣费
    await billing_service.deduct_tokens(
        db, current_user.id, tokens_used,
        f"会话{message_data.session_id}消息",
        str(message_data.session_id)
    )
    
    # 保存AI回复
    ai_message = ChatMessage(
        session_id=message_data.session_id,
        role="assistant",
        content=ai_content,
        tokens_used=tokens_used,
        model="deepseek-chat"
    )
    db.add(ai_message)
    
    await db.commit()
    await db.refresh(ai_message)
    
    return ResponseModel(
        data=ChatMessageResponse.model_validate(ai_message)
    )


@router.post("/messages/stream")
async def send_message_stream(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """发送消息（流式）"""
    # 验证会话
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == message_data.session_id,
            ChatSession.user_id == current_user.id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 获取历史消息
    msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == message_data.session_id)
        .order_by(ChatMessage.created_at)
    )
    history_msgs = msg_result.scalars().all()
    history = [
        {"role": msg.role, "content": msg.content}
        for msg in history_msgs
    ]
    
    # 保存用户消息
    user_message = ChatMessage(
        session_id=message_data.session_id,
        role="user",
        content=message_data.content,
        tokens_used=0
    )
    db.add(user_message)
    await db.commit()
    
    async def generate():
        full_content = ""
        async for chunk in ai_service.chat(message_data.content, history):
            full_content += chunk
            yield f"data: {json.dumps({'content': chunk})}\n\n"
        
        # 计算token并扣费
        tokens_used = len(message_data.content) * 2 + len(full_content) * 2
        
        # 保存AI消息
        ai_message = ChatMessage(
            session_id=message_data.session_id,
            role="assistant",
            content=full_content,
            tokens_used=tokens_used,
            model="deepseek-chat"
        )
        db.add(ai_message)
        
        # 扣费
        await billing_service.deduct_tokens(
            db, current_user.id, tokens_used,
            f"会话{message_data.session_id}消息",
            str(message_data.session_id)
        )
        
        await db.commit()
        
        yield f"data: {json.dumps({'done': True, 'tokens': tokens_used})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

