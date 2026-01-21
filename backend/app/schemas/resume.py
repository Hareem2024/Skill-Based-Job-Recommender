"""
Resume-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResumeBase(BaseModel):
    file_name: str

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    file_path: str
    extracted_text: Optional[str] = None
    extracted_skills: Optional[List[str]] = None
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

