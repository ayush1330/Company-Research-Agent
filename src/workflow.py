from typing import Dict, Any, Optional
from datetime import datetime
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from .models import ResearchState, CompanyBackground, InterviewProcess, PreparationGuide
from .firecrawl import WebResearchService
from .prompts import InterviewResearchPrompts
import json

class Workflow:
    def __init__(self):
        self.firecrawl = WebResearchService()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
        self.prompts = InterviewResearchPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("research_company", self._research_company)
        graph.add_node("research_process", self._research_process)
        graph.add_node("generate_guide", self._generate_guide)
        graph.set_entry_point("research_company")
        graph.add_edge("research_company", "research_process")
        graph.add_edge("research_process", "generate_guide")
        graph.add_edge("generate_guide", END)
        return graph.compile()

    def _research_company(self, state: ResearchState, config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Research company background information"""
        print(f"🔍 Researching company background: {state.company}")
        
        # Build a comprehensive search query
        search_query = (
            f"{state.company} company profile, culture, values, size, industry, "
            f"recent news, funding, leadership, and tech stack"
        )
        
        try:
            # Search for company information
            search_results = self.firecrawl.search_web(
                search_query, 
                num_results=5  # Get more results for better coverage
            )
            
            all_content = []
            processed_urls = set()
            
            for result in search_results[:5]:  # Limit to top 5 results to avoid too many API calls
                try:
                    url = result.get('url') or (result.get('url') if isinstance(result, dict) else None)
                    if not url or url in processed_urls:
                        continue
                        
                    print(f"  🔗 Scraping: {url}")
                    scraped = self.firecrawl.scrape_url(url)
                    
                    if not scraped or not scraped.get('markdown'):
                        continue
                        
                    content = scraped['markdown']
                    if not isinstance(content, str) or len(content) < 50:  # Skip very short or invalid content
                        continue
                        
                    # Add source information
                    source = f"Source: {url}"
                    title = result.get('title') or (result.get('title') if isinstance(result, dict) else None)
                    if title:
                        source = f"{title} | {source}"
                        
                    all_content.append(f"\n{'='*80}\n{source}\n{'='*80}\n{content[:5000]}\n")
                    processed_urls.add(url)
                    
                    # Stop if we have enough content
                    if len(all_content) >= 3:  # Limit to top 3 sources
                        break
                        
                except Exception as e:
                    print(f"  ⚠️ Error processing {url}: {str(e)[:200]}")
            
            # Join all content with separators
            research_content = "\n".join(all_content) if all_content else "No relevant content found."
            print(f"  ✅ Gathered {len(processed_urls)} sources with relevant content")
            
            if not research_content or research_content == "No relevant content found.":
                print("⚠️ No content found during company research")
                return {"background": CompanyBackground()}
            
            # Use the new prompt structure from prompts.py
            try:
                system_prompt = self.prompts.get_company_research_system_prompt()
                user_prompt = self.prompts.get_company_research_user_prompt(state.company, research_content)
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                # Get the LLM response
                response = self.llm.invoke(messages, config=config)
                
                # Clean and parse the response
                content = response.content.strip()
                if '```json' in content:
                    content = content[content.find('```json') + 7:]
                    content = content[:content.rfind('```')].strip()
                
                # Parse the JSON response
                company_data = json.loads(content)
                
                # Create the CompanyBackground object with default values for missing fields
                background = CompanyBackground(
                    company_size=company_data.get('company_size', 'Unknown'),
                    industry=company_data.get('industry', 'Unknown'),
                    company_culture=company_data.get('company_culture', 'Unknown'),
                    values=company_data.get('values', []),
                    recent_news=company_data.get('recent_news', [])
                )
                
                print(f"✅ Successfully extracted company information for {state.company}")
                if processed_urls:
                    sources = list(processed_urls)
                    print(f"   Sources used: {', '.join(sources[:3])}{'...' if len(sources) > 3 else ''}")
                    
                return {"background": background, "research_content": research_content, "sources": sources}
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                if 'response' in locals():
                    print(f"Response content (first 500 chars): {response.content[:500]}...")
                return {"background": CompanyBackground(), "research_content": research_content, "sources": list(processed_urls)}
                
            except Exception as e:
                print(f"❌ Company research analysis failed: {str(e)}")
                return {"background": CompanyBackground(), "research_content": research_content, "sources": list(processed_urls)}
            
        except Exception as e:
            print(f"🔴 Error during company research: {str(e)}")
            return {
                "background": CompanyBackground(
                    company_size="Unknown",
                    industry="Unknown",
                    company_culture="Unknown"
                ),
                "research_content": f"Error: {str(e)[:300]}",
                "sources": []
            }

    def _research_process(self, state: ResearchState, config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Research interview process for specific role"""
        print(f"🔍 Researching interview process: {state.role} at {state.company}")
        
        # Build a comprehensive search query
        search_query = (
            f"{state.company} {state.role} interview process stages questions "
            f"technical assessment coding challenge system design behavioral"
        )
        
        try:
            # Search for interview process information
            search_results = self.firecrawl.search_web(
                search_query,
                num_results=5  # Get more results for better coverage
            )
            
            all_content = []
            processed_urls = set()
            
            for result in search_results[:5]:  # Limit to top 5 results
                try:
                    url = result.get('url') or (result.get('url') if isinstance(result, dict) else None)
                    if not url or url in processed_urls:
                        continue
                        
                    print(f"  🔗 Scraping interview info from: {url}")
                    scraped = self.firecrawl.scrape_url(url)
                    
                    if not scraped or not scraped.get('markdown'):
                        continue
                        
                    content = scraped['markdown']
                    if not isinstance(content, str) or len(content) < 50:  # Skip very short or invalid content
                        continue
                        
                    # Add source information
                    title = result.get('title') or (result.get('title') if isinstance(result, dict) else None)
                    source = f"Source: {url}"
                    if title:
                        source = f"{title} | {source}"
                        
                    all_content.append(f"\n{'='*80}\n{source}\n{'='*80}\n{content[:5000]}\n")
                    processed_urls.add(url)
                    
                    # Stop if we have enough content
                    if len(all_content) >= 3:  # Limit to top 3 sources
                        break
                        
                except Exception as e:
                    print(f"  ⚠️ Error processing {url}: {str(e)[:200]}")
                    
            # Join all content with separators
            research_content = "\n".join(all_content) if all_content else "No relevant content found."
            print(f"  ✅ Gathered {len(processed_urls)} sources with interview information")
            
            if not research_content or research_content == "No relevant content found.":
                print("⚠️ No interview process information found")
                # Return default InterviewProcess with required fields
                return {
                    "interview_process": InterviewProcess(
                        typical_stages=["Unknown"],
                        duration="Unknown",
                        common_questions=[]
                    ),
                    "interview_research_content": research_content,
                    "sources": list(processed_urls)
                }
            
            # Join all content with separators
            research_content = "\n".join(all_content) if all_content else "No relevant interview information found."
            print(f"  ✅ Gathered {len(processed_urls)} sources with interview information")
            
            if not research_content or research_content == "No relevant interview information found.":
                print("⚠️ No interview process information found")
                return {
                    "interview_process": InterviewProcess(
                        typical_stages=["Unknown"],
                        duration="Unknown",
                        common_questions=[]
                    ),
                    "interview_research_content": research_content,
                    "interview_sources": list(processed_urls)
                }
            
            # Use the new prompt structure from prompts.py
            try:
                system_prompt = self.prompts.get_interview_process_system_prompt()
                user_prompt = self.prompts.get_interview_process_user_prompt(
                    state.company, 
                    state.role,
                    research_content
                )
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_prompt)
                ]
                
                # Get the LLM response
                response = self.llm.invoke(messages, config=config)
                
                # Clean and parse the response
                content = response.content.strip()
                if '```json' in content:
                    content = content[content.find('```json') + 7:]
                    content = content[:content.rfind('```')].strip()
                
                # Parse the JSON response
                process_data = json.loads(content)
                
                # Ensure required fields have values and proper types
                typical_stages = ["Initial Screening", "Technical Interview", "Final Round"]
                if isinstance(process_data.get('typical_stages'), list):
                    typical_stages = process_data['typical_stages']
                
                duration = str(process_data.get('duration', '3-6 weeks'))
                
                # Ensure list fields are always lists
                common_questions = process_data.get('common_questions')
                if not isinstance(common_questions, list):
                    common_questions = []
                
                # Create the InterviewProcess object with all required fields
                interview_process = InterviewProcess(
                    typical_stages=typical_stages,
                    duration=duration,
                    common_questions=common_questions,
                    technical_assessment=bool(process_data.get('technical_assessment', False)),
                    system_design=bool(process_data.get('system_design', False)),
                    behavioral_focus=bool(process_data.get('behavioral_focus', False)),
                    coding_challenges=bool(process_data.get('coding_challenges', False)),
                    take_home_projects=bool(process_data.get('take_home_projects', False))
                )
                
                print(f"✅ Successfully extracted interview process for {state.role} at {state.company}")
                if processed_urls:
                    sources = list(processed_urls)
                    print(f"   Sources used: {', '.join(sources[:3])}{'...' if len(sources) > 3 else ''}")
                else:
                    sources = []
                
                return {
                    "interview_process": interview_process,
                    "interview_research_content": research_content,
                    "sources": sources
                }
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ Failed to parse JSON response: {e}")
                if 'response' in locals():
                    print(f"Response content (first 500 chars): {response.content[:500]}...")
                return {
                    "interview_process": InterviewProcess(
                        typical_stages=["Unknown"],
                        duration="Unknown",
                        common_questions=[]
                    ),
                    "interview_research_content": research_content,
                    "sources": list(processed_urls)
                }
                
            except Exception as e:
                print(f"❌ Interview process analysis failed: {str(e)}")
                return {
                    "interview_process": InterviewProcess(
                        typical_stages=["Unknown"],
                        duration="Unknown",
                        common_questions=[]
                    ),
                    "interview_research_content": research_content,
                    "sources": list(processed_urls)
                }
            
        except Exception as e:
            print(f"🔴 Error during interview process research: {str(e)}")
            return {
                "interview_process": InterviewProcess(
                    typical_stages=["Unknown"],
                    duration="Unknown"
                ),
                "interview_research_content": f"Error: {str(e)[:300]}",
                "sources": []
            }
        
        # Get structured interview process info from the research content
        research_data = state.get('interview_research_content', {})
        research_content = research_data.get('interview_research_content', 'No interview content found')
        sources = research_data.get('interview_sources', [])
        
        try:
            # Prepare the prompt with clear instructions and context
            system_prompt = """You are an expert in analyzing technical interview processes. 
            Extract and structure key information about the interview process from the provided research content.
            Be precise and only include information that can be clearly inferred from the content.
            If information is not available, use 'Unknown' rather than making assumptions."""
            
            user_prompt = f"""Analyze the following research content about the interview process for {state.role} at {state.company} and extract the requested information:
            
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
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get the LLM response
            response = self.llm.invoke(messages, config=config)
            
            # Clean and parse the response
            content = response.content.strip()
            if '```json' in content:
                content = content[content.find('```json') + 7:]
                content = content[:content.rfind('```')].strip()
            
            # Parse the JSON response
            process_data = json.loads(content)
            
            # Create the InterviewProcess object with default values for missing fields
            interview_process = InterviewProcess(
                typical_stages=process_data.get('typical_stages', ["Unknown"]),
                duration=process_data.get('duration', 'Unknown'),
                common_questions=process_data.get('common_questions', []),
                technical_assessment=process_data.get('technical_assessment', False),
                system_design=process_data.get('system_design', False),
                behavioral_focus=process_data.get('behavioral_focus', False),
                coding_challenges=process_data.get('coding_challenges', False),
                take_home_projects=process_data.get('take_home_projects', False),
                difficulty_level=process_data.get('difficulty_level', 'Moderate')
            )
            
            print(f"✅ Successfully extracted interview process for {state.role} at {state.company}")
            if sources:
                print(f"   Sources used: {', '.join(sources[:3])}{'...' if len(sources) > 3 else ''}")
                
            return {"interview_process": interview_process}
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            if 'response' in locals():
                print(f"Response content (first 500 chars): {response.content[:500]}...")
            return {"interview_process": InterviewProcess(
                typical_stages=["Unknown"],
                duration="Unknown",
                common_questions=[]
            )}
            
        except Exception as e:
            print(f"❌ Interview process research failed: {str(e)}")
            return {"interview_process": InterviewProcess(
                typical_stages=["Unknown"],
                duration="Unknown",
                common_questions=[]
            )}

    def _generate_guide(self, state: ResearchState, config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Generate a comprehensive preparation guide based on research"""
        print(f"📝 Generating preparation guide for {state.role} at {state.company}")
        
        # Prepare context data with proper error handling
        background = state.background.dict() if state.background else {}
        interview_process = state.interview_process.dict() if state.interview_process else {}
        
        # Get research content and sources for context
        company_research = getattr(state, 'research_content', "No company research available.")
        interview_research = getattr(state, 'interview_research_content', "No interview research available.")
        
        # Get sources for attribution
        company_sources = getattr(state, 'sources', [])
        interview_sources = getattr(state, 'interview_sources', [])
        
        try:
            # Use the new prompt structure from prompts.py
            system_prompt = self.prompts.get_prep_guide_system_prompt()
            user_prompt = self.prompts.get_prep_guide_user_prompt(
                company=state.company,
                role=state.role,
                background=background,
                process=interview_process,
                company_research=company_research,
                interview_research=interview_research
            )
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get the LLM response
            response = self.llm.invoke(messages, config=config)
            
            # Clean and parse the response
            content = response.content.strip()
            
            # Extract JSON if present in markdown code block
            if '```json' in content:
                content = content[content.find('```json') + 7:]
                content = content[:content.rfind('```')].strip()
            
            try:
                # Try to parse as JSON first
                guide_data = json.loads(content)
                
                # Create the guide object with structured data
                preparation_guide = PreparationGuide(
                    overview=guide_data.get('overview', ''),
                    preparation_timeline=guide_data.get('timeline', {}).get('1_week_before', []) +
                                        guide_data.get('timeline', {}).get('3_days_before', []) +
                                        guide_data.get('timeline', {}).get('day_before', []),
                    technical_preparation=guide_data.get('technical_preparation', {}).get('topics_to_study', []),
                    behavioral_preparation=guide_data.get('behavioral_preparation', {}).get('common_questions', []),
                    company_specific_prep=[guide_data.get('behavioral_preparation', {}).get('company_specific_tips', '')],
                    interview_day_tips=[],
                    follow_up=[],
                    additional_resources=guide_data.get('technical_preparation', {}).get('practice_resources', []) +
                                      guide_data.get('additional_tips', []),
                    last_updated=datetime.now().isoformat(),
                    sources={
                        'company_research': company_sources[:5],  # Limit to top 5 sources
                        'interview_research': interview_sources[:5]
                    }
                )
                
                print(f"✅ Successfully generated structured preparation guide for {state.role} at {state.company}")
                return {"preparation_guide": preparation_guide}
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Could not parse guide as JSON, falling back to markdown. Error: {e}")
                # Fall back to using the raw content as markdown
                preparation_guide = PreparationGuide(
                    overview=content,
                    preparation_timeline=[],
                    technical_preparation=[],
                    behavioral_preparation=[],
                    company_specific_prep=[],
                    interview_day_tips=[],
                    follow_up=[],
                    additional_resources=[],
                    last_updated=datetime.now().isoformat(),
                    sources={
                        'company_research': company_sources[:5],
                        'interview_research': interview_sources[:5]
                    }
                )
                
                print(f"⚠️ Generated guide from markdown content (JSON parsing failed) for {state.role} at {state.company}")
                return {"preparation_guide": preparation_guide}
                
        except Exception as e:
            error_msg = f"❌ Guide generation failed: {str(e)}"
            print(error_msg)
            
            # Create a minimal guide with error information
            return {
                "preparation_guide": PreparationGuide(
                    overview=f"# Error Generating Guide\n\n{error_msg}\n\nPlease try again or check the logs for more details.",
                    last_updated=datetime.now().isoformat(),
                    sources={}
                )
            }

    def run(self, company: str, role: str, config: Optional[RunnableConfig] = None) -> ResearchState:
        """Execute the research workflow"""
        initial_state = ResearchState(company=company, role=role)
        final_state = self.workflow.invoke(initial_state, config=config)
        return ResearchState(**final_state)