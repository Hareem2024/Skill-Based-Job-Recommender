"""
Recommendation endpoints for learning roadmaps and projects.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import User, Resume, Recommendation
from app.core.security import get_current_active_user
from app.schemas.recommendation import RecommendationResponse, RecommendationCreate
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter()

@router.post("/roadmap/{resume_id}", response_model=List[RecommendationResponse])
async def generate_roadmap(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate a personalized learning roadmap."""
    # Verify resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Generate recommendations
    engine = RecommendationEngine()
    recommendations = await engine.generate_roadmap(db, resume)
    
    # Save recommendations
    db_recommendations = []
    for rec in recommendations:
        db_rec = Recommendation(
            user_id=current_user.id,
            recommendation_type="roadmap",
            title=rec["title"],
            description=rec["description"],
            priority=rec.get("priority", 0),
            estimated_time=rec.get("estimated_time", ""),
            resources=rec.get("resources", []),
            reasoning=rec.get("reasoning", "")
        )
        db.add(db_rec)
        db_recommendations.append(db_rec)
    
    db.commit()
    
    return db_recommendations

@router.post("/projects/{resume_id}", response_model=List[RecommendationResponse])
async def generate_project_suggestions(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate personalized project suggestions."""
    # Verify resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Generate recommendations
    engine = RecommendationEngine()
    recommendations = await engine.generate_projects(db, resume)
    
    # Save recommendations
    db_recommendations = []
    for rec in recommendations:
        db_rec = Recommendation(
            user_id=current_user.id,
            recommendation_type="project",
            title=rec["title"],
            description=rec["description"],
            priority=rec.get("priority", 0),
            estimated_time=rec.get("estimated_time", ""),
            resources=rec.get("resources", []),
            reasoning=rec.get("reasoning", "")
        )
        db.add(db_rec)
        db_recommendations.append(db_rec)
    
    db.commit()
    
    return db_recommendations

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    recommendation_type: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all recommendations for current user."""
    query = db.query(Recommendation).filter(Recommendation.user_id == current_user.id)
    
    if recommendation_type:
        query = query.filter(Recommendation.recommendation_type == recommendation_type)
    
    recommendations = query.order_by(Recommendation.priority.desc(), Recommendation.created_at.desc()).all()
    return recommendations

@router.get("/{recommendation_id}", response_model=RecommendationResponse)
async def get_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific recommendation."""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    return recommendation

