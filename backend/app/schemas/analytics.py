"""
Analytics-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class SkillTrendResponse(BaseModel):
    id: int
    skill_name: str
    demand_count: int
    date: datetime
    
    class Config:
        from_attributes = True

class SkillAnalyticsResponse(BaseModel):
    top_skills: List[Dict[str, Any]]
    trends: Dict[str, Any]
    period_days: int

