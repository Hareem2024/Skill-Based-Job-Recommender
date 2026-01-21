"""
Skill matching using vector embeddings and similarity.
"""
from typing import Dict, List, Any
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
ML_AVAILABLE = True

class SkillMatcher:
    """Match skills using embeddings."""
    
    def __init__(self):
        # Use a lightweight model for skill matching
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            # Fallback: use simple string matching
            self.model = None
    
    async def calculate_match(
        self,
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str] = None
    ) -> Dict[str, Any]:
        """Calculate match score between resume and job skills."""
        if not resume_skills or not required_skills:
            return {
                "score": 0.0,
                "details": {
                    "matched_required": [],
                    "matched_preferred": [],
                    "missing_required": required_skills
                }
            }
        
        preferred_skills = preferred_skills or []
        
        if self.model:
            # Use embeddings for semantic matching
            return await self._match_with_embeddings(
                resume_skills, required_skills, preferred_skills
            )
        else:
            # Fallback to exact matching
            return await self._match_exact(
                resume_skills, required_skills, preferred_skills
            )
    
    async def _match_with_embeddings(
        self,
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str]
    ) -> Dict[str, Any]:
        """Match using embeddings."""
        # Encode all skills
        all_skills = resume_skills + required_skills + preferred_skills
        embeddings = self.model.encode(all_skills)
        
        resume_embeddings = embeddings[:len(resume_skills)]
        required_embeddings = embeddings[len(resume_skills):len(resume_skills)+len(required_skills)]
        preferred_embeddings = embeddings[len(resume_skills)+len(required_skills):]
        
        # Calculate similarity
        required_similarities = cosine_similarity(resume_embeddings, required_embeddings)
        preferred_similarities = cosine_similarity(resume_embeddings, preferred_embeddings) if len(preferred_embeddings) > 0 else np.array([])
        
        # Find matches (threshold: 0.7)
        threshold = 0.7
        matched_required = []
        matched_preferred = []
        
        for i, req_skill in enumerate(required_skills):
            max_sim = np.max(required_similarities[:, i])
            if max_sim >= threshold:
                matched_idx = np.argmax(required_similarities[:, i])
                matched_required.append({
                    "required": req_skill,
                    "matched": resume_skills[matched_idx],
                    "similarity": float(max_sim)
                })
        
        for i, pref_skill in enumerate(preferred_skills):
            if len(preferred_similarities) > 0:
                max_sim = np.max(preferred_similarities[:, i])
                if max_sim >= threshold:
                    matched_idx = np.argmax(preferred_similarities[:, i])
                    matched_preferred.append({
                        "preferred": pref_skill,
                        "matched": resume_skills[matched_idx],
                        "similarity": float(max_sim)
                    })
        
        # Calculate score
        required_match_ratio = len(matched_required) / len(required_skills) if required_skills else 0
        preferred_match_ratio = len(matched_preferred) / len(preferred_skills) if preferred_skills else 0
        
        # Weighted score: 70% required, 30% preferred
        score = (required_match_ratio * 70) + (preferred_match_ratio * 30)
        
        missing_required = [
            skill for skill in required_skills
            if not any(m["required"] == skill for m in matched_required)
        ]
        
        return {
            "score": round(score, 2),
            "details": {
                "matched_required": matched_required,
                "matched_preferred": matched_preferred,
                "missing_required": missing_required
            }
        }
    
    async def _match_exact(
        self,
        resume_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str]
    ) -> Dict[str, Any]:
        """Match using exact string matching."""
        resume_skills_lower = [s.lower() for s in resume_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        preferred_skills_lower = [s.lower() for s in preferred_skills]
        
        matched_required = [
            skill for skill in required_skills_lower
            if skill in resume_skills_lower
        ]
        
        matched_preferred = [
            skill for skill in preferred_skills_lower
            if skill in resume_skills_lower
        ]
        
        required_match_ratio = len(matched_required) / len(required_skills) if required_skills else 0
        preferred_match_ratio = len(matched_preferred) / len(preferred_skills) if preferred_skills else 0
        
        score = (required_match_ratio * 70) + (preferred_match_ratio * 30)
        
        missing_required = [
            skill for skill in required_skills
            if skill.lower() not in resume_skills_lower
        ]
        
        return {
            "score": round(score, 2),
            "details": {
                "matched_required": [{"required": s, "matched": s} for s in matched_required],
                "matched_preferred": [{"preferred": s, "matched": s} for s in matched_preferred],
                "missing_required": missing_required
            }
        }

