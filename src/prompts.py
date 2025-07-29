from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

class InterviewResearchPrompts:
    """Collection of prompts for researching company interview processes"""

    # ===== COMPANY RESEARCH PROMPTS =====
    @staticmethod
    def get_company_research_system_prompt() -> str:
        return """You are an expert researcher specializing in company research for job candidates. 
        Extract and structure key information about the company from the provided research content.
        Be precise and only include information that can be clearly inferred from the content.
        If information is not available, use 'Unknown' rather than making assumptions."""

    @staticmethod
    def get_company_research_user_prompt(company: str, research_content: str) -> str:
        return f"""Analyze the following research content about {company} and extract the requested information:
        
        ===== RESEARCH CONTENT =====
        {research_content}
        ===== END OF CONTENT =====
        
        Extract the following information as a JSON object with these exact field names:
        {{
            "company_size": "Estimated number of employees (e.g., '1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5001-10000', '10001+')",
            "industry": "Primary industry or industries the company operates in",
            "company_culture": "A brief description of the company culture (1-2 sentences)",
            "values": ["List", "of", "core", "values"],
            "recent_news": ["List", "of", "recent", "news", "or", "developments"]
        }}
        
        Only respond with the JSON object, nothing else. Ensure the response is valid JSON."""

    # ===== INTERVIEW PROCESS PROMPTS =====
    @staticmethod
    def get_interview_process_system_prompt() -> str:
        return """You are an expert in analyzing technical interview processes. 
        Extract and structure key information about the interview process from the provided research content.
        Be precise and only include information that can be clearly inferred from the content.
        If information is not available, use null rather than making assumptions."""

    @staticmethod
    def get_interview_process_user_prompt(company: str, role: str, research_content: str) -> str:
        return f"""Analyze the following research content about the interview process for {role} at {company} and extract the requested information:
        
        ===== RESEARCH CONTENT =====
        {research_content}
        ===== END OF CONTENT =====
        
        Extract the following information as a JSON object with these exact field names:
        {{
            "typical_stages": ["List", "of", "typical", "interview", "stages"],
            "duration": "Estimated duration from first contact to offer (e.g., '2-4 weeks')",
            "common_questions": ["List", "of", "commonly", "asked", "questions"],
            "technical_assessment": true/false,
            "system_design": true/false,
            "behavioral_focus": true/false,
            "coding_challenges": true/false,
            "take_home_projects": true/false,
            "difficulty_level": "Easy/Moderate/Difficult"
        }}
        
        Only respond with the JSON object, nothing else. Ensure the response is valid JSON.
        If a field cannot be determined, use null for that field."""

    # ===== PREPARATION GUIDE PROMPTS =====
    @staticmethod
    def get_prep_guide_system_prompt() -> str:
        return """You are an expert career coach and technical interviewer. 
        Create a comprehensive, actionable preparation guide for a candidate based on the provided 
        company and interview process information. Provide specific, practical advice that would 
        help a candidate succeed in their interview process."""

    @staticmethod
    def get_prep_guide_user_prompt(company: str, role: str, background: Dict[str, Any], process: Dict[str, Any]) -> str:
        background_str = json.dumps(background, indent=2, ensure_ascii=False)
        process_str = json.dumps(process, indent=2, ensure_ascii=False)
        
        return f"""Create a detailed preparation guide for a {role} position at {company}.
        
        COMPANY BACKGROUND:
        {background_str}
        
        INTERVIEW PROCESS:
        {process_str}
        
        INSTRUCTIONS:
        1. Create a structured guide with clear sections and actionable steps
        2. Include specific preparation strategies based on the company's interview process
        3. Provide technical study recommendations if technical assessments are mentioned
        4. Include behavioral preparation tips if behavioral interviews are part of the process
        5. Suggest resources for further study (e.g., books, online courses, practice platforms)
        6. Include general interview tips and best practices
        
        FORMAT YOUR RESPONSE AS A JSON OBJECT with these fields:
        {{
            "overview": "Brief overview of the preparation strategy",
            "timeline": {{
                "1_week_before": ["List", "of", "actions"],
                "3_days_before": ["List", "of", "actions"],
                "day_before": ["List", "of", "actions"],
                "interview_day": ["List", "of", "actions"]
            }},
            "technical_preparation": {{
                "topics_to_study": ["List", "of", "topics"],
                "practice_resources": ["List", "of", "resources"],
                "project_ideas": ["List", "of", "project", "ideas"]
            }},
            "behavioral_preparation": {{
                "common_questions": ["List", "of", "questions"],
                "star_method_tips": "Tips for using the STAR method",
                "company_specific_tips": "Specific advice for this company"
            }},
            "additional_tips": ["List", "of", "additional", "tips"]
        }}
        
        Only respond with the JSON object, nothing else. Ensure the response is valid JSON."""

    # ===== LEGACY PROMPTS (for backward compatibility) =====
    # These will be gradually phased out
    BACKGROUND_SYSTEM = property(get_company_research_system_prompt)
    PROCESS_SYSTEM = property(get_interview_process_system_prompt)
    PREP_SYSTEM = property(get_prep_guide_system_prompt)
    
    @staticmethod
    def background_user(company: str) -> str:
        return InterviewResearchPrompts.get_company_research_user_prompt(company, "")
    
    # ===== PREPARATION GUIDE PROMPTS =====
    @staticmethod
    def get_prep_guide_system_prompt() -> str:
        return """You are an expert career coach and technical interviewer. 
        Create a comprehensive, actionable preparation guide for a candidate based on the provided 
        company and interview process information. Provide specific, practical advice that would 
        help a candidate succeed in their interview process."""

    @staticmethod
    def get_prep_guide_user_prompt(company: str, role: str, background: Dict[str, Any], 
                                 process: Dict[str, Any], company_research: str, 
                                 interview_research: str) -> str:
        """Generate a user prompt for creating a preparation guide."""
        return f"""Create a detailed preparation guide for a {role} position at {company}.
        
        ===== COMPANY BACKGROUND =====
        {json.dumps(background, indent=2, ensure_ascii=False)}
        
        ===== INTERVIEW PROCESS =====
        {json.dumps(process, indent=2, ensure_ascii=False)}
        
        ===== RESEARCH CONTENT =====
        {company_research}
        
        ===== INTERVIEW RESEARCH =====
        {interview_research}
        
        INSTRUCTIONS:
        1. Create a structured guide with clear sections and actionable steps
        2. Include specific preparation strategies based on the company's interview process
        3. Provide technical study recommendations if technical assessments are mentioned
        4. Include behavioral preparation tips if behavioral interviews are part of the process
        5. Suggest resources for further study (e.g., books, online courses, practice platforms)
        6. Include general interview tips and best practices
        
        FORMAT YOUR RESPONSE AS A JSON OBJECT with these fields:
        {{
            "overview": "Brief overview of the preparation strategy",
            "timeline": {{
                "1_week_before": ["Task 1", "Task 2"],
                "3_days_before": ["Task 1", "Task 2"],
                "day_before": ["Task 1", "Task 2"]
            }},
            "technical_preparation": {{
                "topics_to_study": ["List", "of", "topics"],
                "practice_resources": ["List", "of", "resources"],
                "project_ideas": ["List", "of", "project", "ideas"]
            }},
            "behavioral_preparation": {{
                "common_questions": ["List", "of", "questions"],
                "star_method_tips": "Tips for using the STAR method",
                "company_specific_tips": "Specific advice for this company"
            }},
            "additional_tips": ["List", "of", "additional", "tips"]
        }}
        
        Only respond with the JSON object, nothing else. Ensure the response is valid JSON."""

    # Helper methods for backward compatibility
    @staticmethod
    def process_user(company: str, role: str) -> str:
        return InterviewResearchPrompts.get_interview_process_user_prompt(company, role, "")
    
    @staticmethod
    def prep_user(company: str, role: str, background: Dict[str, Any], process: Dict[str, Any]) -> str:
        return InterviewResearchPrompts.get_prep_guide_user_prompt(company, role, background, process)