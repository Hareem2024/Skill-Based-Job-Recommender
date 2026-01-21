"""
AI chatbot endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.db.database import get_db
from app.db.models import User, ChatMessage
from app.core.security import get_current_active_user
from app.services.chatbot import AIChatbot

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    message_id: int

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Chat with AI mentor."""
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    # Get chatbot response
    chatbot = AIChatbot()
    response = await chatbot.get_response(db, current_user, request.message)
    
    # Save message
    db_message = ChatMessage(
        user_id=current_user.id,
        message=request.message,
        response=response
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return ChatResponse(response=response, message_id=db_message.id)

@router.get("/history")
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get chat history for current user."""
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    return [{"message": m.message, "response": m.response, "created_at": m.created_at} for m in messages]

