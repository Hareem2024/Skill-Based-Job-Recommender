"""
Job posting-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class JobPostingBase(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None

class JobPostingResponse(JobPostingBase):
    id: int
    source_url: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    scraped_at: datetime
    
    class Config:
        from_attributes = True

class JobMatchResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    match_score: float
    skill_match_details: Optional[Dict[str, Any]] = None
    missing_skills: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

