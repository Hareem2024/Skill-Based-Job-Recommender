"""
Resume upload and processing endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import User, Resume
from app.core.security import get_current_active_user
from app.schemas.resume import ResumeResponse, ResumeCreate
from app.services.resume_parser import ResumeParser
from app.core.config import settings
import aiofiles
from pathlib import Path

router = APIRouter()

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload and process a resume."""
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Save file
    file_path = settings.UPLOAD_DIR / f"{current_user.id}_{file.filename}"
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large"
            )
        await f.write(content)
    
    # Parse resume
    parser = ResumeParser()
    parsed_data = await parser.parse_resume(str(file_path))
    
    # Create resume record
    db_resume = Resume(
        user_id=current_user.id,
        file_path=str(file_path),
        file_name=file.filename,
        extracted_text=parsed_data.get("text", ""),
        extracted_skills=parsed_data.get("skills", []),
        parsed_data=parsed_data
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume

@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all resumes for current user."""
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific resume."""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    return resume

