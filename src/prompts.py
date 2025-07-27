class InterviewResearchPrompts:
    """Collection of prompts for researching company interview processes"""

    # Company background research prompts
    BACKGROUND_SYSTEM = """You are an expert researcher specializing in company research for job candidates. 
                        Extract key information about the company that is relevant to interview preparation."""

    @staticmethod
    def background_user(company: str) -> str:
        return f"""Company: {company}
        Extract the following information from available sources:
        - Company size (number of employees)
        - Industry and primary business focus
        - Company culture description (3-5 key adjectives)
        - Core values (list 3-5 values)
        - Recent news/events affecting hiring (last 6 months)

        Format your response as JSON with keys: 
        company_size, industry, company_culture, values, recent_news"""

    # Interview process research prompts
    PROCESS_SYSTEM = """You are an expert in analyzing interview processes. Focus on extracting details 
                      relevant to software engineering candidates. Pay special attention to technical 
                      assessments and behavioral expectations."""

    @staticmethod
    def process_user(company: str, role: str) -> str:
        return f"""Company: {company}
        Role: {role}
        
        Analyze the typical interview process and provide:
        - List of typical interview stages (e.g., phone screen, technical round, system design)
        - Estimated duration from first contact to offer
        - List of 5-7 common technical questions
        - List of 5-7 common behavioral questions
        - Flags indicating if they use: 
          * technical_assessment (coding tests)
          * system_design (architecture questions)
          * behavioral_focus (culture-fit questions)
          * coding_challenges (live coding)
          * take_home_projects
        
        Format your response as JSON with keys:
        typical_stages, duration, common_questions, technical_assessment, 
        system_design, behavioral_focus, coding_challenges, take_home_projects"""

    # Preparation guide generation prompts
    PREP_SYSTEM = """You are a senior hiring manager with 15+ years of experience at top tech companies. 
                   Create actionable, specific preparation advice for candidates. Focus on practical 
                   strategies rather than generic advice."""

    @staticmethod
    def prep_user(company: str, role: str, background: dict, process: dict) -> str:
        return f"""Company: {company} | Role: {role}
        
        Company Background:
        - Size: {background.get('company_size', 'N/A')}
        - Industry: {background.get('industry', 'N/A')}
        - Culture: {background.get('company_culture', 'N/A')}
        - Values: {', '.join(background.get('values', []))}
        - Recent News: {', '.join(background.get('recent_news', []))}
        
        Interview Process:
        - Stages: {', '.join(process.get('typical_stages', []))}
        - Duration: {process.get('duration', 'N/A')}
        - Technical Assessment: {'Yes' if process.get('technical_assessment') else 'No'}
        - System Design: {'Yes' if process.get('system_design') else 'No'}
        - Behavioral Focus: {'Yes' if process.get('behavioral_focus') else 'No'}
        
        Create a preparation guide covering:
        1. Technical Topics: List 5-7 specific technical areas to focus on (programming languages, frameworks, concepts)
        2. Behavioral Topics: List 3-5 key behavioral/values-based areas to prepare stories for
        3. Resources: Recommend 3-5 specific resources (books, courses, practice platforms)
        4. Strategy: 2-3 sentence preparation strategy addressing company's specific process
        5. Common Pitfalls: 3-4 common mistakes candidates make in this company's process
        
        Format your response as JSON with keys:
        technical_topics, behavioral_topics, resources, strategy, common_pitfalls"""