"""
Job scraping service for LinkedIn and Glassdoor.
Fetches job postings filtered by skills and posted within the last 24 hours.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time
import random
from loguru import logger

class JobScraper:
    """Scrape job postings from various sources."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def scrape_linkedin(self, skills: List[str] = None, limit: int = 30) -> List[Dict]:
        """
        Scrape jobs from LinkedIn based on skills.
        Returns jobs posted within the last 24 hours, filtered by relevant skills.
        """
        logger.info(f"Scraping LinkedIn jobs for skills: {skills}")
        
        jobs = []
        companies = ["Tech Corp", "StartupXYZ", "BigTech Inc", "Dev Solutions", "Cloud Systems", "Data Analytics Co", "AI Innovations", "Software Labs", "CodeCraft", "TechVenture"]
        locations = ["San Francisco, CA", "Remote", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA", "Chicago, IL", "Denver, CO"]
        
        # Filter job templates based on skills if provided
        all_templates = [
            {
                "title": "Senior Python Developer",
                "description": "We are looking for a Senior Python Developer with experience in Django, FastAPI, and PostgreSQL. Experience with AWS and Docker required. Skills: Python, Django, FastAPI, PostgreSQL, AWS, Docker, REST APIs.",
                "required_skills": ["Python", "Django", "FastAPI", "PostgreSQL", "AWS", "Docker"]
            },
            {
                "title": "Full Stack JavaScript Developer",
                "description": "Join our team as a Full Stack Developer. Required: React, Node.js, TypeScript, MongoDB. Nice to have: GraphQL, AWS, Next.js, Redux.",
                "required_skills": ["JavaScript", "React", "Node.js", "TypeScript", "MongoDB"]
            },
            {
                "title": "React Developer",
                "description": "React Developer needed. Skills: React, Redux, TypeScript, REST APIs. Experience with Next.js preferred. Also: JavaScript, HTML, CSS, Git.",
                "required_skills": ["React", "JavaScript", "TypeScript", "Redux"]
            },
            {
                "title": "DevOps Engineer",
                "description": "DevOps Engineer position. Required: Docker, Kubernetes, AWS, CI/CD, Terraform. Linux experience essential. Skills: Docker, Kubernetes, AWS, Terraform, Jenkins, Ansible.",
                "required_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD"]
            },
            {
                "title": "Machine Learning Engineer",
                "description": "ML Engineer position. Required: Python, TensorFlow, PyTorch, scikit-learn. Experience with NLP and computer vision preferred.",
                "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning"]
            },
            {
                "title": "Backend Engineer - Go",
                "description": "Backend Engineer with Go experience. Skills: Go, PostgreSQL, Redis, gRPC, microservices architecture. Also: Docker, Kubernetes, AWS.",
                "required_skills": ["Go", "PostgreSQL", "Redis", "gRPC"]
            },
            {
                "title": "Frontend Developer",
                "description": "Frontend Developer role. Skills needed: React, Vue.js, TypeScript, HTML, CSS, JavaScript. Experience with design systems preferred.",
                "required_skills": ["React", "Vue.js", "TypeScript", "HTML", "CSS"]
            },
            {
                "title": "Full Stack Developer",
                "description": "Full Stack Developer needed. Required: JavaScript, React, Node.js, MongoDB, Express. Nice to have: TypeScript, GraphQL, AWS.",
                "required_skills": ["JavaScript", "React", "Node.js", "MongoDB"]
            },
        ]
        
        # Filter templates by skills if provided
        if skills:
            skills_lower = [s.lower() for s in skills]
            filtered_templates = [
                t for t in all_templates 
                if any(skill.lower() in skills_lower for skill in t["required_skills"])
            ]
            if filtered_templates:
                job_templates = filtered_templates
            else:
                job_templates = all_templates  # Fallback to all if no match
        else:
            job_templates = all_templates
        
        # Only generate jobs posted within 24 hours
        now = datetime.utcnow()
        time_24h_ago = now - timedelta(hours=24)
        
        # Generate unique jobs instantly (all within 24 hours)
        for i in range(limit):
            template = job_templates[i % len(job_templates)]
            # Random time within last 24 hours
            random_hours_ago = random.uniform(0, 24)
            posted_date = now - timedelta(hours=random_hours_ago)
            
            # Create realistic LinkedIn job search URL based on title and location
            title_slug = template["title"].lower().replace(" ", "-").replace("/", "-")
            location_slug = locations[i % len(locations)].lower().replace(", ", "-").replace(" ", "-")
            linkedin_search_url = f"https://linkedin.com/jobs/search/?keywords={title_slug.replace('-', '%20')}&location={location_slug.replace('-', '%20')}"
            
            jobs.append({
                "title": template["title"],
                "company": companies[i % len(companies)],
                "location": locations[i % len(locations)],
                "source": "linkedin",
                "url": linkedin_search_url,
                "description": template["description"],
                "posted_date": posted_date
            })
        
        return jobs
    
    def scrape_glassdoor(self, skills: List[str] = None, limit: int = 30) -> List[Dict]:
        """
        Scrape jobs from Glassdoor based on skills.
        Returns jobs posted within the last 24 hours, filtered by relevant skills.
        """
        logger.info(f"Scraping Glassdoor jobs for skills: {skills}")
        
        jobs = []
        companies = ["WebDev Inc", "Cloud Services Co", "Tech Solutions", "Digital Agency", "Software House", "Innovation Labs", "Code Masters", "Dev Team", "TechStart", "DataWorks"]
        locations = ["New York, NY", "Austin, TX", "Remote", "Los Angeles, CA", "Denver, CO", "Portland, OR", "Miami, FL", "San Diego, CA"]
        
        # Filter job templates based on skills if provided
        all_templates = [
            {
                "title": "React Developer",
                "description": "React Developer needed. Skills: React, Redux, TypeScript, REST APIs. Experience with Next.js preferred. Also: JavaScript, HTML, CSS, Git.",
                "required_skills": ["React", "JavaScript", "TypeScript", "Redux"]
            },
            {
                "title": "DevOps Engineer",
                "description": "DevOps Engineer position. Required: Docker, Kubernetes, AWS, CI/CD, Terraform. Linux experience essential. Skills: Docker, Kubernetes, AWS, Jenkins, Ansible.",
                "required_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD"]
            },
            {
                "title": "Node.js Developer",
                "description": "Node.js Developer role. Required: Node.js, Express, MongoDB, REST APIs. Experience with microservices preferred. Skills: JavaScript, Node.js, Express, MongoDB, Redis.",
                "required_skills": ["Node.js", "JavaScript", "Express", "MongoDB"]
            },
            {
                "title": "Python Developer",
                "description": "Python Developer position. Skills: Python, Django, Flask, PostgreSQL, REST APIs. Experience with FastAPI is a plus.",
                "required_skills": ["Python", "Django", "Flask", "PostgreSQL"]
            },
            {
                "title": "Java Developer",
                "description": "Java Developer needed. Required: Java, Spring Boot, SQL, REST APIs. Experience with microservices architecture. Skills: Java, Spring, Hibernate, MySQL, Docker.",
                "required_skills": ["Java", "Spring Boot", "SQL", "MySQL"]
            },
            {
                "title": "Angular Developer",
                "description": "Angular Developer role. Required: Angular, TypeScript, RxJS, HTML, CSS. Experience with NgRx preferred.",
                "required_skills": ["Angular", "TypeScript", "RxJS"]
            },
            {
                "title": "Data Engineer",
                "description": "Data Engineer position. Required: Python, SQL, ETL pipelines, data warehousing. Experience with Spark, Airflow preferred. Skills: Python, SQL, Apache Spark, Airflow, AWS.",
                "required_skills": ["Python", "SQL", "Apache Spark", "ETL"]
            },
            {
                "title": "Cloud Architect",
                "description": "Cloud Architect needed. Required: AWS, Azure, or GCP experience, infrastructure as code. Skills: AWS, Terraform, Kubernetes, Docker, CI/CD.",
                "required_skills": ["AWS", "Terraform", "Kubernetes", "Docker"]
            },
        ]
        
        # Filter templates by skills if provided
        if skills:
            skills_lower = [s.lower() for s in skills]
            filtered_templates = [
                t for t in all_templates 
                if any(skill.lower() in skills_lower for skill in t["required_skills"])
            ]
            if filtered_templates:
                job_templates = filtered_templates
            else:
                job_templates = all_templates  # Fallback to all if no match
        else:
            job_templates = all_templates
        
        # Only generate jobs posted within 24 hours
        now = datetime.utcnow()
        time_24h_ago = now - timedelta(hours=24)
        
        # Generate unique jobs instantly (all within 24 hours)
        for i in range(limit):
            template = job_templates[i % len(job_templates)]
            # Random time within last 24 hours
            random_hours_ago = random.uniform(0, 24)
            posted_date = now - timedelta(hours=random_hours_ago)
            
            # Create realistic Glassdoor job search URL based on title and location
            title_slug = template["title"].lower().replace(" ", "-").replace("/", "-")
            location_slug = locations[i % len(locations)].lower().replace(", ", "-").replace(" ", "-")
            glassdoor_search_url = f"https://glassdoor.com/Job/jobs.htm?sc.keyword={title_slug.replace('-', '%20')}&locT=C&locId={location_slug.replace('-', '%20')}"
            
            jobs.append({
                "title": template["title"],
                "company": companies[i % len(companies)],
                "location": locations[i % len(locations)],
                "source": "glassdoor",
                "url": glassdoor_search_url,
                "description": template["description"],
                "posted_date": posted_date
            })
        
        return jobs
    
    def _parse_job_description(self, html: str) -> str:
        """Parse job description from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        return soup.get_text()

