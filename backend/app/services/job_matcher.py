"""
Job matching service using ML embeddings and similarity.
"""
from typing import Dict, List, Any
from app.db.models import Resume, JobPosting
from app.ml.skill_matcher import SkillMatcher

class JobMatcher:
    """Match resumes to job postings."""
    
    def __init__(self):
        self.skill_matcher = SkillMatcher()
    
    async def match(self, resume: Resume, job: JobPosting) -> Dict[str, Any]:
        """Match a resume to a job posting."""
        resume_skills = resume.extracted_skills or []
        job_required = job.required_skills or []
        job_preferred = job.preferred_skills or []
        
        # Calculate match score
        match_result = await self.skill_matcher.calculate_match(
            resume_skills=resume_skills,
            required_skills=job_required,
            preferred_skills=job_preferred
        )
        
        # Find missing skills
        missing_skills = [skill for skill in job_required if skill not in resume_skills]
        
        return {
            "score": match_result["score"],
            "details": match_result["details"],
            "missing_skills": missing_skills
        }

