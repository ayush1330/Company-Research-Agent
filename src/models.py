from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class CompanyBackground(BaseModel):
    """Company background information relevant to interview preparation"""
    company_size: str  # e.g., "500-1000 employees"
    industry: str
    company_culture: str
    values: List[str] = []
    recent_news: List[str] = []

class InterviewProcess(BaseModel):
    """Structured information about a company's interview process"""
    typical_stages: List[str] = []  # e.g., ["Phone Screen", "Technical Interview", "System Design", "Behavioral"]
    duration: str  # e.g., "2-4 weeks"
    common_questions: List[str] = []
    technical_assessment: bool = False
    system_design: bool = False
    behavioral_focus: bool = False
    coding_challenges: bool = False
    take_home_projects: bool = False

class PreparationGuide(BaseModel):
    """Actionable preparation guide for candidates"""
    technical_topics: List[str] = []
    behavioral_topics: List[str] = []
    resources: List[str] = []  # URLs to study resources
    strategy: str = ""  # Preparation strategy summary
    common_pitfalls: List[str] = []

class ResearchState(BaseModel):
    """State container for interview research workflow"""
    company: str
    role: str
    background: Optional[CompanyBackground] = None
    interview_process: Optional[InterviewProcess] = None
    preparation_guide: Optional[PreparationGuide] = None
    search_results: List[Dict[str, Any]] = []  # Raw search data