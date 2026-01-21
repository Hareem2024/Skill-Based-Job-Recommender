"""
AI chatbot service for interactive mentoring.
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.db.models import User, Resume, Recommendation
from app.ml.chatbot_llm import ChatbotLLM

class AIChatbot:
    """AI-powered chatbot for mentoring."""
    
    def __init__(self):
        self.llm = ChatbotLLM()
    
    async def get_response(self, db: Session, user: User, message: str) -> str:
        """Get AI response to user message."""
        # Get user context
        latest_resume = db.query(Resume).filter(
            Resume.user_id == user.id
        ).order_by(Resume.created_at.desc()).first()
        
        recent_recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == user.id
        ).order_by(Recommendation.created_at.desc()).limit(5).all()
        
        # Build context
        context = {
            "user_name": user.full_name or user.email,
            "resume_skills": latest_resume.extracted_skills if latest_resume else [],
            "recent_recommendations": [
                {"title": r.title, "type": r.recommendation_type}
                for r in recent_recommendations
            ]
        }
        
        # Get LLM response
        response = await self.llm.get_response(message, context)
        
        return response

