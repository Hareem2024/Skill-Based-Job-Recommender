"""
Skill extraction from text using fast keyword matching.
"""
import re
from typing import List, Set

class SkillExtractor:
    """Extract skills from text using NLP."""
    
    def __init__(self):
        # Common tech skills database
        self.tech_skills = {
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
            "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl",
            # Web Technologies
            "html", "css", "react", "vue", "angular", "node.js", "express", "django",
            "flask", "spring", "asp.net", "laravel", "rails", "next.js", "nuxt",
            # Databases
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
            "sqlite", "oracle", "sql server", "dynamodb", "neo4j",
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "ci/cd",
            "terraform", "ansible", "linux", "bash", "shell scripting",
            # ML/AI
            "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
            "pandas", "numpy", "opencv", "nlp", "computer vision",
            # Mobile
            "android", "ios", "react native", "flutter", "xamarin",
            # Other
            "graphql", "rest api", "microservices", "agile", "scrum", "git"
        }
        
        # Skip spaCy loading for faster performance - use simple keyword matching only
        self.nlp = None
    
    async def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text - fast keyword matching."""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = set()
        
        # Fast direct matching against skill database (no NLP processing)
        for skill in self.tech_skills:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Also check for common abbreviations and variations
        skill_variations = {
            "js": "javascript",
            "ts": "typescript", 
            "node": "node.js",
            "reactjs": "react",
            "vuejs": "vue",
            "postgres": "postgresql",
            "ml": "machine learning",
            "dl": "deep learning",
            "cv": "computer vision",
            "sql": "sql",
            "api": "rest api"
        }
        
        for abbrev, full_name in skill_variations.items():
            if abbrev in text_lower and full_name in self.tech_skills:
                found_skills.add(full_name)
        
        # Normalize skills (handle variations)
        normalized_skills = self._normalize_skills(list(found_skills))
        
        return normalized_skills
    
    def _normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalize skill names (handle variations)."""
        # Skill normalization mapping
        normalization_map = {
            "js": "javascript",
            "ts": "typescript",
            "node": "node.js",
            "reactjs": "react",
            "vuejs": "vue",
            "postgres": "postgresql",
            "ml": "machine learning",
            "dl": "deep learning",
            "cv": "computer vision"
        }
        
        normalized = []
        for skill in skills:
            skill_lower = skill.lower()
            # Check if skill needs normalization
            if skill_lower in normalization_map:
                normalized.append(normalization_map[skill_lower])
            else:
                normalized.append(skill)
        
        # Remove duplicates and sort
        return sorted(list(set(normalized)))

