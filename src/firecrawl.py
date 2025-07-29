import os
import time
from typing import List, Dict, Any, Optional
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

class WebResearchService:
    def __init__(self):
        """Initialize the WebResearchService with Firecrawl API key."""
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)
        self.last_request_time = 0
        self.min_request_interval = 2.0  # Minimum seconds between requests

    def _rate_limit(self):
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the web using Firecrawl.
        
        Args:
            query: The search query string
            num_results: Maximum number of results to return
            
        Returns:
            List of search results with metadata
        """
        self._rate_limit()
        
        try:
            result = self.app.search(
                query=query,
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            
            # Convert result to a list of dictionaries if it's not already
            if hasattr(result, 'data'):
                result = result.data
            
            if isinstance(result, list):
                return [self._clean_result(r) for r in result]
            elif isinstance(result, dict):
                return [self._clean_result(result)]
            return []
            
        except Exception as e:
            print(f"🔴 Firecrawl search error: {str(e)[:500]}")
            return []

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a single URL using Firecrawl.
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dictionary containing scraped content and metadata
        """
        self._rate_limit()
        
        try:
            scraped = self.app.scrape_url(
                url,
                formats=["markdown"]
            )
            
            # Ensure we return a consistent dictionary format
            if hasattr(scraped, 'markdown'):
                return {"markdown": scraped.markdown, "url": url}
            elif isinstance(scraped, dict):
                return {"markdown": scraped.get("markdown", ""), "url": url, **scraped}
            return {"markdown": "", "url": url}
            
        except Exception as e:
            error_msg = str(e)[:500]  # Truncate long error messages
            print(f"🔴 Error scraping {url}: {error_msg}")
            return {"markdown": "", "url": url, "error": error_msg}
    
    def _clean_result(self, result: Any) -> Dict[str, Any]:
        """Convert a result object to a clean dictionary."""
        if isinstance(result, dict):
            return result
        elif hasattr(result, 'dict'):
            return result.dict()
        elif hasattr(result, '__dict__'):
            return vars(result)
        return {"content": str(result)}

    def get_content_from_results(self, results: List[Dict[str, Any]], max_chars: int = 2500, max_urls: int = 5) -> str:
        """
        Extract and combine content from search results with rate limiting.
        
        Args:
            results: List of search result dictionaries
            max_chars: Maximum number of characters to return
            max_urls: Maximum number of URLs to process
            
        Returns:
            Combined content from multiple sources as a single string
        """
        all_content = []
        total_chars = 0
        processed_urls = 0
        
        for result in results:
            # Check if we've reached our limits
            if total_chars >= max_chars or processed_urls >= max_urls:
                break
                
            if not result or not isinstance(result, dict):
                continue
                
            url = result.get("url", "").strip()
            if not url or len(url) > 500:  # Skip invalid or suspiciously long URLs
                continue
                
            try:
                # Scrape the URL (rate limiting is handled in scrape_url)
                scraped = self.scrape_url(url)
                
                if scraped and scraped.get("markdown"):
                    content = scraped["markdown"].strip()
                    if content:
                        # Calculate remaining characters we can add
                        remaining_chars = max_chars - total_chars
                        if remaining_chars <= 0:
                            break
                            
                        # Truncate content if needed
                        if len(content) > remaining_chars:
                            content = content[:remaining_chars] + "..."
                        
                        # Add source attribution
                        source = f"## Source: {url}\n\n{content}\n"
                        all_content.append(source)
                        total_chars += len(source)
                        processed_urls += 1
                        
                        print(f"✅ Processed {url} ({len(content)} chars, {processed_urls}/{min(len(results), max_urls)} URLs)")
                        
            except Exception as e:
                error_msg = str(e)[:200]  # Truncate long error messages
                print(f"⚠️ Error processing {url}: {error_msg}")
                continue
        
        combined = "\n\n".join(all_content)
        print(f"📊 Processed {processed_urls} URLs, total {len(combined)} characters")
        return combined