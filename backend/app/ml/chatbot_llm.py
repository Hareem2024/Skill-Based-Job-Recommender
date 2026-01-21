"""
LLM-powered chatbot for AI mentoring.
"""
import openai
from typing import Dict, Any
from app.core.config import settings

class ChatbotLLM:
    """AI chatbot using LLM."""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def get_response(self, message: str, context: Dict[str, Any]) -> str:
        """Get chatbot response."""
        if not settings.OPENAI_API_KEY:
            return self._fallback_response(message, context)
        
        try:
            # Build context string
            context_str = f"""User: {context.get('user_name', 'User')}
Current Skills: {', '.join(context.get('resume_skills', [])[:10])}
Recent Recommendations: {', '.join([r['title'] for r in context.get('recent_recommendations', [])])}"""
            
            prompt = f"""You are an AI career mentor helping developers. Use this context:
{context_str}

User Question: {message}

Provide a helpful, encouraging response. Be specific and actionable."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly and knowledgeable career mentor for software developers. Help them with learning paths, project suggestions, and career advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return self._fallback_response(message, context)
    
    def _fallback_response(self, message: str, context: Dict[str, Any]) -> str:
        """Fallback response without LLM."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["project", "build", "create"]):
            return "I'd suggest starting with a project that combines your current skills with something new you want to learn. Check your recommendations for specific project ideas!"
        
        elif any(word in message_lower for word in ["learn", "study", "skill"]):
            skills = context.get('resume_skills', [])
            if skills:
                return f"Based on your skills ({', '.join(skills[:3])}), I'd recommend focusing on technologies that complement what you already know. Check your learning roadmap for personalized suggestions!"
            return "I'd recommend checking your personalized learning roadmap for skill suggestions tailored to your goals."
        
        elif any(word in message_lower for word in ["job", "career", "hire"]):
            return "Focus on building projects that showcase the skills in demand for your target roles. Your skill match scores can help identify areas to improve!"
        
        else:
            return "I'm here to help with your learning journey! Ask me about projects, skills to learn, or career advice. You can also check your personalized recommendations and learning roadmap."

