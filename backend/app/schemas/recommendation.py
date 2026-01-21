"""
Recommendation-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class RecommendationBase(BaseModel):
    title: str
    description: Optional[str] = None

class RecommendationCreate(RecommendationBase):
    recommendation_type: str
    priority: int = 0
    estimated_time: Optional[str] = None
    resources: Optional[List[str]] = None
    reasoning: Optional[str] = None

class RecommendationResponse(RecommendationBase):
    id: int
    user_id: int
    recommendation_type: str
    priority: int
    estimated_time: Optional[str] = None
    resources: Optional[List[str]] = None
    reasoning: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

