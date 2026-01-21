"""
AI-powered recommendation engine for learning roadmaps and projects.
"""
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.db.models import Resume, JobPosting, JobMatch
from app.ml.recommender import MLRecommender

class RecommendationEngine:
    """Generate personalized recommendations."""
    
    def __init__(self):
        self.ml_recommender = MLRecommender()
    
    async def generate_roadmap(self, db: Session, resume: Resume) -> List[Dict[str, Any]]:
        """Generate a personalized learning roadmap."""
        resume_skills = resume.extracted_skills or []
        
        # Get top job matches to understand skill gaps
        matches = db.query(JobMatch).filter(
            JobMatch.resume_id == resume.id
        ).order_by(JobMatch.match_score.desc()).limit(10).all()
        
        # Collect missing skills from top matches
        all_missing_skills = []
        for match in matches:
            if match.missing_skills:
                all_missing_skills.extend(match.missing_skills)
        
        # If no job matches, use common in-demand skills as missing skills
        if not all_missing_skills:
            # Common skills that are often in demand
            common_skills = [
                "Machine Learning", "Cloud Computing", "Docker", "Kubernetes",
                "AWS", "Python", "React", "Node.js", "Database Design",
                "System Design", "API Development", "DevOps", "CI/CD"
            ]
            # Filter out skills they already have
            all_missing_skills = [skill for skill in common_skills if skill.lower() not in [s.lower() for s in resume_skills]]
            # If still empty, just use common skills
            if not all_missing_skills:
                all_missing_skills = common_skills[:7]
        
        # Use ML to generate roadmap
        roadmap = await self.ml_recommender.generate_learning_roadmap(
            current_skills=resume_skills,
            missing_skills=list(set(all_missing_skills))
        )
        
        return roadmap
    
    async def generate_projects(self, db: Session, resume: Resume) -> List[Dict[str, Any]]:
        """Generate personalized project suggestions."""
        resume_skills = resume.extracted_skills or []
        
        # Get top job matches
        matches = db.query(JobMatch).filter(
            JobMatch.resume_id == resume.id
        ).order_by(JobMatch.match_score.desc()).limit(5).all()
        
        # Collect skills from desired jobs
        target_skills = set()
        for match in matches:
            job = match.job
            if job.required_skills:
                target_skills.update(job.required_skills)
            if job.preferred_skills:
                target_skills.update(job.preferred_skills)
        
        # If no job matches, use resume skills + common next steps
        if not target_skills:
            # Build on existing skills with common next steps
            common_next_steps = [
                "Full Stack Development", "RESTful API", "Database Optimization",
                "Microservices", "Testing & QA", "Performance Optimization",
                "Security Best Practices", "Agile Development", "Version Control"
            ]
            # Combine resume skills with next steps
            target_skills = set(resume_skills + common_next_steps)
        
        # Use ML to generate project suggestions
        projects = await self.ml_recommender.generate_project_suggestions(
            current_skills=resume_skills,
            target_skills=list(target_skills)
        )
        
        return projects

