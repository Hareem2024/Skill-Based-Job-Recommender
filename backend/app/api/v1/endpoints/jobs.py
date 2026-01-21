"""
Job posting endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.db.database import get_db, SessionLocal
from app.db.models import User, JobPosting, Resume, JobMatch, SkillTrend
from app.core.security import get_current_active_user
from app.schemas.job import JobPostingResponse, JobMatchResponse
from app.tasks.scraping import scrape_jobs_task
from app.services.job_matcher import JobMatcher
from app.services.job_scraper import JobScraper
from app.ml.skill_extractor import SkillExtractor
from loguru import logger
import asyncio

router = APIRouter()

@router.get("/", response_model=List[JobPostingResponse])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    source: Optional[str] = None,
    title: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get job postings with optional filters. Only shows LinkedIn and Glassdoor jobs posted within 24 hours."""
    query = db.query(JobPosting)
    
    # Only show jobs posted within 24 hours
    time_24h_ago = datetime.utcnow() - timedelta(hours=24)
    query = query.filter(JobPosting.posted_date >= time_24h_ago)
    
    # Exclude StackOverflow and Indeed jobs, only show LinkedIn and Glassdoor
    query = query.filter(JobPosting.source.in_(["linkedin", "glassdoor"]))
    
    if source:
        query = query.filter(JobPosting.source == source)
    if title:
        query = query.filter(JobPosting.title.ilike(f"%{title}%"))
    
    jobs = query.order_by(JobPosting.posted_date.desc()).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobPostingResponse)
async def get_job(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific job posting."""
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    return job

def run_scraping_sync(user_id: int = None, resume_id: int = None):
    """Run scraping synchronously based on user's resume skills (only LinkedIn and Glassdoor, within 24 hours)."""
    db = SessionLocal()
    scraper = JobScraper()
    
    try:
        # Get user's resume skills
        skills = []
        if resume_id:
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            if resume and resume.extracted_skills:
                skills = resume.extracted_skills
        elif user_id:
            # Get latest resume for user
            resume = db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).first()
            if resume and resume.extracted_skills:
                skills = resume.extracted_skills
        
        logger.info(f"Scraping jobs for skills: {skills}")
        
        all_jobs = []
        
        # Scrape from LinkedIn and Glassdoor only (filtered by skills, within 24 hours)
        logger.info("Scraping LinkedIn...")
        linkedin_jobs = scraper.scrape_linkedin(skills=skills, limit=20)
        all_jobs.extend(linkedin_jobs)
        
        logger.info("Scraping Glassdoor...")
        glassdoor_jobs = scraper.scrape_glassdoor(skills=skills, limit=20)
        all_jobs.extend(glassdoor_jobs)
        
        # Filter jobs posted within 24 hours - ensure all jobs are within 24 hours
        now = datetime.utcnow()
        time_24h_ago = now - timedelta(hours=24)
        filtered_jobs = [
            job for job in all_jobs 
            if job.get("posted_date") and job["posted_date"] >= time_24h_ago
        ]
        
        logger.info(f"Found {len(filtered_jobs)} jobs posted within 24 hours out of {len(all_jobs)} total")
        
        # Double check - remove any jobs older than 24 hours
        filtered_jobs = [job for job in filtered_jobs if (now - job["posted_date"]).total_seconds() <= 86400]
        
        # Save jobs to database
        saved_count = 0
        for job_data in filtered_jobs:
            try:
                # Check if job already exists
                existing = db.query(JobPosting).filter(
                    JobPosting.source_url == job_data.get("url")
                ).first()
                
                if existing:
                    continue
                
                # Extract skills from job description (quick simple extraction)
                description = job_data.get("description", "")
                # Simple keyword-based skill extraction for speed
                skills = []
                skill_keywords = {
                    "Python", "JavaScript", "React", "Node.js", "TypeScript", "Java", "Go", "C++", "C#",
                    "Django", "Flask", "FastAPI", "Express", "Spring", "Angular", "Vue.js",
                    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQL",
                    "AWS", "Docker", "Kubernetes", "Terraform", "CI/CD", "Jenkins",
                    "TensorFlow", "PyTorch", "Machine Learning", "ML", "NLP",
                    "Git", "Linux", "REST APIs", "GraphQL", "gRPC", "microservices"
                }
                description_lower = description.lower()
                for skill in skill_keywords:
                    if skill.lower() in description_lower:
                        skills.append(skill)
                
                # Limit to top 10 skills for performance
                skills = skills[:10]
                
                # Create job posting
                job = JobPosting(
                    title=job_data.get("title", ""),
                    company=job_data.get("company", ""),
                    location=job_data.get("location", ""),
                    source=job_data.get("source", ""),
                    source_url=job_data.get("url", ""),
                    description=description,
                    required_skills=skills,
                    posted_date=job_data.get("posted_date"),
                )
                
                db.add(job)
                db.commit()
                db.refresh(job)
                
                # Create skill trend entries
                for skill in skills:
                    trend = SkillTrend(
                        skill_name=skill,
                        job_id=job.id,
                        demand_count=1,
                        date=datetime.utcnow()
                    )
                    db.add(trend)
                
                db.commit()
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving job: {e}")
                db.rollback()
                continue
        
        logger.info(f"Scraping completed. Saved {saved_count} new jobs.")
        return {"status": "success", "jobs_saved": saved_count}
        
    except Exception as e:
        logger.error(f"Error in scraping: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@router.post("/scrape")
async def trigger_scraping(
    background_tasks: BackgroundTasks,
    resume_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Trigger job scraping task based on user's resume skills. Only LinkedIn and Glassdoor, jobs within 24 hours."""
    # Verify resume belongs to user if provided
    if resume_id:
        resume = db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id
        ).first()
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user has any resume
    if not resume_id:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
        if not resume:
            raise HTTPException(
                status_code=400, 
                detail="Please upload a resume first to scrape relevant jobs"
            )
        resume_id = resume.id
    
    try:
        # Try to use Celery if available
        task = scrape_jobs_task.delay()
        return {"message": "Scraping started (background task)", "task_id": task.id}
    except Exception as e:
        # Fallback to synchronous scraping in background
        logger.warning(f"Celery not available, using background task instead: {e}")
        background_tasks.add_task(run_scraping_sync, user_id=current_user.id, resume_id=resume_id)
        return {
            "message": "Scraping started (synchronous mode)", 
            "note": "Finding jobs matching your resume skills from LinkedIn and Glassdoor (posted within 24 hours)"
        }

@router.get("/matches/{resume_id}", response_model=List[JobMatchResponse])
async def get_job_matches(
    resume_id: int,
    min_score: float = Query(0.0, ge=0.0, le=100.0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get job matches for a resume."""
    # Verify resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get matches
    matches = db.query(JobMatch).filter(
        JobMatch.resume_id == resume_id,
        JobMatch.match_score >= min_score
    ).order_by(JobMatch.match_score.desc()).all()
    
    return matches

@router.post("/match/{resume_id}")
async def match_resume_to_jobs(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Match a resume against all job postings."""
    # Verify resume belongs to user
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Get all jobs
    jobs = db.query(JobPosting).all()
    
    # Match using JobMatcher
    matcher = JobMatcher()
    matches = []
    
    for job in jobs:
        match_result = await matcher.match(resume, job)
        if match_result["score"] > 0:
            # Check if match already exists
            existing_match = db.query(JobMatch).filter(
                JobMatch.resume_id == resume_id,
                JobMatch.job_id == job.id
            ).first()
            
            if existing_match:
                existing_match.match_score = match_result["score"]
                existing_match.skill_match_details = match_result["details"]
                existing_match.missing_skills = match_result["missing_skills"]
            else:
                db_match = JobMatch(
                    resume_id=resume_id,
                    job_id=job.id,
                    match_score=match_result["score"],
                    skill_match_details=match_result["details"],
                    missing_skills=match_result["missing_skills"]
                )
                db.add(db_match)
                matches.append(db_match)
    
    db.commit()
    
    return {"message": f"Matched {len(matches)} jobs", "matches": len(matches)}

@router.delete("/cleanup-old-jobs")
async def cleanup_old_jobs(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove old StackOverflow/Indeed jobs and jobs older than 24 hours. Admin only."""
    try:
        # Remove StackOverflow and Indeed jobs
        deleted_stackoverflow = db.query(JobPosting).filter(JobPosting.source == "stackoverflow").delete()
        deleted_indeed = db.query(JobPosting).filter(JobPosting.source == "indeed").delete()
        
        # Remove jobs older than 24 hours
        time_24h_ago = datetime.utcnow() - timedelta(hours=24)
        deleted_old = db.query(JobPosting).filter(JobPosting.posted_date < time_24h_ago).delete()
        
        db.commit()
        
        return {
            "message": "Cleanup completed",
            "deleted_stackoverflow": deleted_stackoverflow,
            "deleted_indeed": deleted_indeed,
            "deleted_old_jobs": deleted_old
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error cleaning up jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

