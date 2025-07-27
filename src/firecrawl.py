import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

class WebResearchService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web for relevant content"""
        try:
            result = self.app.search(
                query=query,
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"],
                    include_images=False
                )
            )
            return result.get("data", [])
        except Exception as e:
            print(f"Firecrawl search error: {e}")
            return []

    def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape content from a specific URL"""
        try:
            result = self.app.scrape_url(
                url,
                options=ScrapeOptions(
                    formats=["markdown"],
                    include_images=False,
                    page_options={"onlyMainContent": True}
                )
            )
            return result
        except Exception as e:
            print(f"Firecrawl scrape error: {e}")
            return None

    def get_content_from_results(self, results: List[Dict[str, Any]], max_chars: int = 2500) -> str:
        """Extract and combine content from search results"""
        all_content = ""
        for result in results:
            url = result.get("url", "")
            if not url:
                continue
                
            scraped = self.scrape_url(url)
            if scraped and scraped.get("markdown"):
                content = scraped["markdown"]
                # Truncate to avoid token limits
                all_content += content[:max_chars] + "\n\n"
                
                # Stop if we have enough content
                if len(all_content) > 6000:
                    break
                    
        return all_content