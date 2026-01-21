"""
Analytics and trend analysis endpoints.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, desc

from app.db.database import get_db
from app.db.models import User, SkillTrend, JobPosting
from app.core.security import get_current_active_user
from app.schemas.analytics import SkillTrendResponse, SkillAnalyticsResponse
from app.services.trend_analyzer import TrendAnalyzer

router = APIRouter()

@router.get("/skills", response_model=SkillAnalyticsResponse)
async def get_skill_analytics(
    days: int = Query(30, ge=1, le=365),
    top_n: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get skill demand analytics."""
    # Calculate date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get top skills by demand
    skill_counts = db.query(
        SkillTrend.skill_name,
        func.count(SkillTrend.id).label('count')
    ).filter(
        SkillTrend.date >= start_date
    ).group_by(
        SkillTrend.skill_name
    ).order_by(
        desc('count')
    ).limit(top_n).all()
    
    skills_data = [{"skill": skill, "demand_count": count} for skill, count in skill_counts]
    
    # Get trend analysis
    analyzer = TrendAnalyzer()
    trends = await analyzer.analyze_trends(db, days=days)
    
    return {
        "top_skills": skills_data,
        "trends": trends,
        "period_days": days
    }

@router.get("/skills/{skill_name}/trend", response_model=List[SkillTrendResponse])
async def get_skill_trend(
    skill_name: str,
    days: int = Query(90, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get trend data for a specific skill."""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    trends = db.query(SkillTrend).filter(
        SkillTrend.skill_name == skill_name,
        SkillTrend.date >= start_date
    ).order_by(SkillTrend.date).all()
    
    return trends

@router.get("/demand-forecast")
async def get_demand_forecast(
    skill_name: Optional[str] = None,
    days_ahead: int = Query(30, ge=1, le=180),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get demand forecast for skills."""
    analyzer = TrendAnalyzer()
    
    if skill_name:
        forecast = await analyzer.forecast_skill_demand(db, skill_name, days_ahead)
        return {"skill": skill_name, "forecast": forecast}
    else:
        # Forecast for top skills
        top_skills = db.query(
            SkillTrend.skill_name,
            func.count(SkillTrend.id).label('count')
        ).group_by(
            SkillTrend.skill_name
        ).order_by(
            desc('count')
        ).limit(10).all()
        
        forecasts = {}
        for skill, _ in top_skills:
            forecast = await analyzer.forecast_skill_demand(db, skill, days_ahead)
            forecasts[skill] = forecast
        
        return {"forecasts": forecasts}

