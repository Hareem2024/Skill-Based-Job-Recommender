"""
Trend analysis service for skill demand forecasting.
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import SkillTrend
from app.ml.trend_forecaster import TrendForecaster

class TrendAnalyzer:
    """Analyze and forecast skill trends."""
    
    def __init__(self):
        self.forecaster = TrendForecaster()
    
    async def analyze_trends(self, db: Session, days: int = 30) -> Dict[str, Any]:
        """Analyze skill trends over a period."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily skill counts
        daily_counts = db.query(
            func.date(SkillTrend.date).label('date'),
            SkillTrend.skill_name,
            func.count(SkillTrend.id).label('count')
        ).filter(
            SkillTrend.date >= start_date
        ).group_by(
            func.date(SkillTrend.date),
            SkillTrend.skill_name
        ).all()
        
        # Organize by skill
        trends_by_skill = {}
        for date, skill, count in daily_counts:
            if skill not in trends_by_skill:
                trends_by_skill[skill] = []
            trends_by_skill[skill].append({"date": date.isoformat(), "count": count})
        
        # Calculate growth rates
        growth_rates = {}
        for skill, data in trends_by_skill.items():
            if len(data) >= 2:
                first_count = data[0]["count"]
                last_count = data[-1]["count"]
                if first_count > 0:
                    growth = ((last_count - first_count) / first_count) * 100
                    growth_rates[skill] = growth
        
        return {
            "daily_trends": trends_by_skill,
            "growth_rates": growth_rates
        }
    
    async def forecast_skill_demand(self, db: Session, skill_name: str, days_ahead: int) -> Dict[str, Any]:
        """Forecast skill demand for the next N days."""
        # Get historical data
        start_date = datetime.utcnow() - timedelta(days=90)
        trends = db.query(SkillTrend).filter(
            SkillTrend.skill_name == skill_name,
            SkillTrend.date >= start_date
        ).order_by(SkillTrend.date).all()
        
        if len(trends) < 7:  # Need at least a week of data
            return {"error": "Insufficient historical data"}
        
        # Prepare data for forecasting
        dates = [t.date for t in trends]
        counts = [t.demand_count for t in trends]
        
        # Use ML forecaster
        forecast = await self.forecaster.forecast(dates, counts, days_ahead)
        
        return {
            "skill": skill_name,
            "forecast": forecast,
            "current_demand": counts[-1] if counts else 0
        }

