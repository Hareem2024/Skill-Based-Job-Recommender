"""
ML-powered recommendation engine using LLMs.
"""
from typing import List, Dict, Any
from openai import OpenAI
from app.core.config import settings

class MLRecommender:
    """Generate recommendations using LLM."""
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_learning_roadmap(
        self,
        current_skills: List[str],
        missing_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate a personalized learning roadmap."""
        if not settings.OPENAI_API_KEY:
            # Fallback recommendations without LLM
            return self._fallback_roadmap(missing_skills)
        
        try:
            prompt = f"""Generate a personalized learning roadmap for a developer with the following:
Current Skills: {', '.join(current_skills[:10])}
Missing Skills: {', '.join(missing_skills[:10])}

Provide 5-7 learning recommendations in JSON format:
[
  {{
    "title": "Skill or topic name",
    "description": "Why this is important and what to learn",
    "priority": 1-10,
    "estimated_time": "e.g., 2 weeks",
    "resources": ["resource1", "resource2"],
    "reasoning": "Why this recommendation was made"
  }}
]

Focus on practical, actionable steps. Return only valid JSON."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert career mentor helping developers learn new skills."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            import json
            content = response.choices[0].message.content
            # Extract JSON from response
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                roadmap = json.loads(content[json_start:json_end])
                return roadmap
        except Exception as e:
            print(f"Error generating roadmap with LLM: {e}")
        
        # Fallback
        return self._fallback_roadmap(missing_skills)
    
    async def generate_project_suggestions(
        self,
        current_skills: List[str],
        target_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate personalized project suggestions."""
        if not settings.OPENAI_API_KEY:
            return self._fallback_projects(current_skills, target_skills)
        
        try:
            prompt = f"""Suggest 5-7 practical projects for a developer to build:
Current Skills: {', '.join(current_skills[:10])}
Target Skills to Learn: {', '.join(target_skills[:10])}

Provide project suggestions in JSON format:
[
  {{
    "title": "Project name",
    "description": "What to build and what skills it teaches",
    "priority": 1-10,
    "estimated_time": "e.g., 1 month",
    "resources": ["tutorial1", "documentation"],
    "reasoning": "Why this project helps learn the target skills"
  }}
]

Return only valid JSON."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert mentor suggesting practical coding projects."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            import json
            content = response.choices[0].message.content
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                projects = json.loads(content[json_start:json_end])
                return projects
        except Exception as e:
            print(f"Error generating projects with LLM: {e}")
        
        return self._fallback_projects(current_skills, target_skills)
    
    def _fallback_roadmap(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Fallback roadmap without LLM."""
        roadmap = []
        
        # If no missing skills provided, use default recommendations
        if not missing_skills:
            missing_skills = [
                "Advanced Problem Solving", "System Design", "Cloud Platforms",
                "Container Technologies", "CI/CD Pipelines", "Database Management",
                "API Development"
            ]
        
        for i, skill in enumerate(missing_skills[:7]):
            roadmap.append({
                "title": f"Learn {skill}",
                "description": f"Master {skill} through hands-on practice and tutorials. This is a valuable skill that will enhance your developer profile.",
                "priority": 10 - i,
                "estimated_time": "2-4 weeks",
                "resources": [
                    f"{skill} official documentation",
                    f"{skill} tutorial on YouTube",
                    f"{skill} online course"
                ],
                "reasoning": f"This skill is in high demand and will improve your job prospects"
            })
        return roadmap
    
    def _fallback_projects(self, current_skills: List[str], target_skills: List[str]) -> List[Dict[str, Any]]:
        """Fallback projects without LLM."""
        projects = []
        
        # If no target skills, create projects based on current skills
        if not target_skills:
            target_skills = current_skills if current_skills else ["Web Development", "Database", "API"]
        
        # Default project ideas if we still have nothing
        if not target_skills:
            target_skills = [
                "Full Stack Web Application", "REST API", "Database-Driven App",
                "Real-time Application", "Mobile App", "Data Analytics Tool",
                "Automation Script"
            ]
        
        for i, skill in enumerate(target_skills[:7]):
            projects.append({
                "title": f"Build a {skill} Application",
                "description": f"Create a practical project using {skill} to reinforce your learning. This hands-on project will help you master the concepts.",
                "priority": 10 - i,
                "estimated_time": "3-4 weeks",
                "resources": [
                    f"{skill} project ideas",
                    f"{skill} best practices guide",
                    f"{skill} tutorial resources"
                ],
                "reasoning": f"Building a project with {skill} will help you learn by doing and add valuable experience to your portfolio"
            })
        return projects

