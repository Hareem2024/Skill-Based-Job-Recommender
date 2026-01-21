"""
Resume parsing service using NLP and document parsing.
"""
import pdfplumber
from docx import Document
from pathlib import Path
from typing import Dict, List, Any
import re
from app.ml.skill_extractor import SkillExtractor

class ResumeParser:
    """Parse resumes and extract information."""
    
    def __init__(self):
        # Initialize skill extractor (now fast, no spaCy loading)
        self.skill_extractor = SkillExtractor()
    
    async def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse a resume file and extract information - optimized for speed."""
        file_ext = Path(file_path).suffix.lower()
        
        # Extract text based on file type (fast extraction)
        if file_ext == '.pdf':
            text = self._extract_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = self._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Extract skills using fast keyword matching (no heavy NLP)
        skills = await self.skill_extractor.extract_skills(text)
        
        # Extract other information (fast regex-based)
        parsed_data = {
            "text": text[:5000],  # Limit text size for storage
            "skills": skills,
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text)
        }
        
        return parsed_data
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            raise ValueError(f"Error extracting PDF: {str(e)}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error extracting DOCX: {str(e)}")
        return text
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text."""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else ""
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information."""
        education_keywords = ['university', 'college', 'degree', 'bachelor', 'master', 'phd', 'education']
        lines = text.split('\n')
        education_lines = [line for line in lines if any(keyword in line.lower() for keyword in education_keywords)]
        return education_lines[:5]  # Return top 5 matches
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience information."""
        experience_keywords = ['experience', 'worked', 'employed', 'position', 'role', 'developer', 'engineer']
        lines = text.split('\n')
        experience_lines = [line for line in lines if any(keyword in line.lower() for keyword in experience_keywords)]
        return experience_lines[:10]  # Return top 10 matches

