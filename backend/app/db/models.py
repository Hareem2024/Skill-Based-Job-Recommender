"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    resumes = relationship("Resume", back_populates="owner")
    recommendations = relationship("Recommendation", back_populates="user")

class Resume(Base):
    """Resume model."""
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    extracted_text = Column(Text)
    extracted_skills = Column(JSON)  # List of skills
    parsed_data = Column(JSON)  # Full parsed resume data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="resumes")
    matches = relationship("JobMatch", back_populates="resume")

class JobPosting(Base):
    """Job posting model."""
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    company = Column(String, index=True)
    location = Column(String)
    source = Column(String)  # linkedin, indeed, stackoverflow
    source_url = Column(String, unique=True)
    description = Column(Text)
    required_skills = Column(JSON)  # List of skills
    preferred_skills = Column(JSON)  # List of skills
    experience_level = Column(String)  # junior, mid, senior
    salary_range = Column(String)
    posted_date = Column(DateTime(timezone=True))
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    matches = relationship("JobMatch", back_populates="job")
    skill_trends = relationship("SkillTrend", back_populates="job")

class JobMatch(Base):
    """Job-resume match model."""
    __tablename__ = "job_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    match_score = Column(Float, nullable=False)  # 0-100
    skill_match_details = Column(JSON)  # Detailed matching info
    missing_skills = Column(JSON)  # Skills user lacks
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    resume = relationship("Resume", back_populates="matches")
    job = relationship("JobPosting", back_populates="matches")

class Recommendation(Base):
    """Learning roadmap and project recommendations."""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommendation_type = Column(String)  # roadmap, project, skill
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=0)  # Higher = more important
    estimated_time = Column(String)  # e.g., "2 weeks", "1 month"
    resources = Column(JSON)  # List of resources/links
    reasoning = Column(Text)  # Why this is recommended
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")

class SkillTrend(Base):
    """Skill demand trend data."""
    __tablename__ = "skill_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("job_postings.id"))
    demand_count = Column(Integer, default=1)
    date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("JobPosting", back_populates="skill_trends")

class ChatMessage(Base):
    """AI chatbot conversation messages."""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")

