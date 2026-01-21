"""
Application configuration using Pydantic settings.
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    PROJECT_NAME: str = "Intelligent Developer Hiring Portal"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/hiring_portal"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3040"]
    
    # File uploads
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".doc"]
    
    # Scraping
    SCRAPING_INTERVAL_HOURS: int = 6
    MAX_JOBS_PER_SCRAPE: int = 100
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        case_sensitive = True

# Create uploads directory if it doesn't exist
settings = Settings()
settings.UPLOAD_DIR.mkdir(exist_ok=True)

