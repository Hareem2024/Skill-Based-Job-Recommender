"""
Job scraping tasks using Celery.
"""
from app.celery_app import celery_app
from app.services.job_scraper import JobScraper
from app.db.database import SessionLocal
from app.db.models import JobPosting, SkillTrend
from app.ml.skill_extractor import SkillExtractor
from loguru import logger
from datetime import datetime

@celery_app.task(name="app.tasks.scraping.scrape_jobs_task")
def scrape_jobs_task():
    """Scrape jobs from all sources."""
    logger.info("Starting job scraping task...")
    
    db = SessionLocal()
    scraper = JobScraper()
    skill_extractor = SkillExtractor()
    
    try:
        all_jobs = []
        
        # Scrape from each source
        logger.info("Scraping LinkedIn...")
        linkedin_jobs = scraper.scrape_linkedin(limit=30)
        all_jobs.extend(linkedin_jobs)
        
        logger.info("Scraping Indeed...")
        indeed_jobs = scraper.scrape_indeed(limit=30)
        all_jobs.extend(indeed_jobs)
        
        logger.info("Scraping StackOverflow...")
        stackoverflow_jobs = scraper.scrape_stackoverflow(limit=30)
        all_jobs.extend(stackoverflow_jobs)
        
        # Save jobs to database
        saved_count = 0
        for job_data in all_jobs:
            try:
                # Check if job already exists
                existing = db.query(JobPosting).filter(
                    JobPosting.source_url == job_data.get("url")
                ).first()
                
                if existing:
                    continue
                
                # Extract skills from job description
                description = job_data.get("description", "")
                import asyncio
                skills = asyncio.run(skill_extractor.extract_skills(description))
                
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
        logger.error(f"Error in scraping task: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

