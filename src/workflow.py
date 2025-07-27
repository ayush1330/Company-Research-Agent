from typing import Dict, Any, Optional
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
        
        # Search for company information
        search_results = self.firecrawl.search_web(
            f"{state.company} culture values size industry recent news", 
            num_results=3
        )
        
        all_content = ""
        for result in search_results:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_url(url)
            if scraped and scraped.get("markdown"):
                all_content += scraped["markdown"][:2000] + "\n\n"
        
        # Get structured background info
        messages = [
            SystemMessage(content=self.prompts.BACKGROUND_SYSTEM),
            HumanMessage(content=self.prompts.background_user(state.company))
        ]
        
        try:
            response = self.llm.invoke(messages, config=config)
            background_data = json.loads(response.content.strip())
            background = CompanyBackground(**background_data)
            print(f"✅ Found background info for {state.company}")
            return {"background": background}
        except Exception as e:
            print(f"❌ Background research failed: {e}")
            return {"background": CompanyBackground(
                company_size="Unknown",
                industry="Unknown",
                company_culture="Unknown"
            )}

    def _research_process(self, state: ResearchState, config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Research interview process for specific role"""
        print(f"🔍 Researching interview process: {state.role} at {state.company}")
        
        # Search for interview process information
        search_results = self.firecrawl.search_web(
            f"{state.company} {state.role} interview process questions", 
            num_results=4
        )
        
        all_content = ""
        for result in search_results:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_url(url)
            if scraped and scraped.get("markdown"):
                all_content += scraped["markdown"][:2500] + "\n\n"
        
        # Get structured process info
        messages = [
            SystemMessage(content=self.prompts.PROCESS_SYSTEM),
            HumanMessage(content=self.prompts.process_user(state.company, state.role))
        ]
        
        try:
            response = self.llm.invoke(messages, config=config)
            process_data = json.loads(response.content.strip())
            interview_process = InterviewProcess(**process_data)
            print(f"✅ Found interview process info for {state.role}")
            return {"interview_process": interview_process}
        except Exception as e:
            print(f"❌ Process research failed: {e}")
            return {"interview_process": InterviewProcess(
                typical_stages=["Unknown"],
                duration="Unknown",
                common_questions=[]
            )}

    def _generate_guide(self, state: ResearchState, config: Optional[RunnableConfig] = None) -> Dict[str, Any]:
        """Generate preparation guide based on research"""
        print(f"📝 Generating preparation guide for {state.role} at {state.company}")
        
        # Prepare context data
        background_data = state.background.dict() if state.background else {}
        process_data = state.interview_process.dict() if state.interview_process else {}
        
        # Generate preparation guide
        messages = [
            SystemMessage(content=self.prompts.PREP_SYSTEM),
            HumanMessage(content=self.prompts.prep_user(
                state.company, 
                state.role, 
                background_data, 
                process_data
            ))
        ]
        
        try:
            response = self.llm.invoke(messages, config=config)
            guide_data = json.loads(response.content.strip())
            preparation_guide = PreparationGuide(**guide_data)
            print(f"✅ Preparation guide created")
            return {"preparation_guide": preparation_guide}
        except Exception as e:
            print(f"❌ Guide generation failed: {e}")
            return {"preparation_guide": PreparationGuide(
                strategy="Failed to generate guide"
            )}

    def run(self, company: str, role: str, config: Optional[RunnableConfig] = None) -> ResearchState:
        """Execute the research workflow"""
        initial_state = ResearchState(company=company, role=role)
        final_state = self.workflow.invoke(initial_state, config=config)
        return ResearchState(**final_state)