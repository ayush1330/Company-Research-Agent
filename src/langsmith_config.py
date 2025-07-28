"""
LangSmith configuration and utilities for the interview-research-agent project.
"""
import os
from typing import Optional, Dict, Any
from langsmith import Client
from langchain_core.runnables import RunnableConfig
import uuid

class LangSmithConfig:
    """Configuration class for LangSmith integration"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.is_enabled = False
        self.project_name = "interview-research-agent"
        
    def setup(self, api_key: Optional[str] = None) -> bool:
        """
        Setup LangSmith configuration
        
        Args:
            api_key: LangSmith API key (optional, can be set via environment)
            
        Returns:
            bool: True if setup was successful, False otherwise
        """
        try:
            # Set required environment variables
            if not os.getenv("LANGCHAIN_TRACING_V2"):
                os.environ["LANGCHAIN_TRACING_V2"] = "true"
            
            if not os.getenv("LANGCHAIN_ENDPOINT"):
                os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
            
            if not os.getenv("LANGCHAIN_PROJECT"):
                # Use a consistent project name by default, but allow override via environment variable
                os.environ["LANGCHAIN_PROJECT"] = self.project_name
            
            # Set API key if provided
            if api_key and not os.getenv("LANGCHAIN_API_KEY"):
                os.environ["LANGCHAIN_API_KEY"] = api_key
            
            # Initialize client
            self.client = Client()
            self.is_enabled = True
            print(f"✅ LangSmith tracing enabled | Project: {os.getenv('LANGCHAIN_PROJECT')}")
            return True
            
        except Exception as e:
            print(f"⚠️ LangSmith setup failed: {e}")
            self.is_enabled = False
            return False
    
    def create_config(self, 
                     company: str, 
                     role: str, 
                     tags: Optional[list] = None, 
                     metadata: Optional[Dict[str, Any]] = None) -> RunnableConfig:
        """
        Create a RunnableConfig with LangSmith tracing enabled
        
        Args:
            company: Company being researched
            role: Job role being applied for
            tags: Additional tags for the trace
            metadata: Additional metadata for the trace
            
        Returns:
            RunnableConfig: Configuration object for tracing
        """
        config_tags = ["interview-research"]
        if tags:
            config_tags.extend(tags)
            
        config_metadata = {
            "company": company,
            "role": role
        }
        if metadata:
            config_metadata.update(metadata)
            
        return RunnableConfig(
            tags=config_tags,
            metadata=config_metadata
        )
    
    def get_trace_url(self, run_id: str) -> str:
        """
        Generate a URL to view the trace in LangSmith
        
        Args:
            run_id: The run ID from the trace
            
        Returns:
            str: URL to view the trace
        """
        return f"https://smith.langchain.com/runs/{run_id}"
    
    def list_recent_traces(self, limit: int = 5):
        """
        List recent traces from LangSmith
        
        Args:
            limit: Maximum number of traces to return
        """
        if not self.client or not self.is_enabled:
            print("LangSmith is not enabled")
            return
            
        try:
            runs = self.client.list_runs(limit=limit)
            print(f"\n📊 Recent research traces:")
            for i, run in enumerate(runs, 1):
                company = run.metadata.get("company", "Unknown")
                role = run.metadata.get("role", "Unknown")
                print(f"{i}. {company} ({role}) - {run.status} - {run.start_time}")
                if run.id:
                    print(f"   URL: {self.get_trace_url(run.id)}")
        except Exception as e:
            print(f"Error listing traces: {e}")


# Global instance
langsmith_config = LangSmithConfig()