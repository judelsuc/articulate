"""
Research Agent and related tools for gathering web information.
"""
from typing import Optional
from openai import OpenAI
from src.config import Config


class PerplexityResearchTool:
    """Tool for searching the web using Perplexity API via OpenAI-compatible client"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.PERPLEXITY_API_KEY
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=Config.PERPLEXITY_API_URL
        )
        self.model = Config.PERPLEXITY_MODEL
        
        # Track usage across calls
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_calls = 0
    
    def search(self, query: str) -> str:
        """
        Search for information using Perplexity API
        
        Args:
            query: Search query string
            
        Returns:
            Research findings as string
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            # Track usage
            if hasattr(response, 'usage') and response.usage:
                self.total_prompt_tokens += response.usage.prompt_tokens
                self.total_completion_tokens += response.usage.completion_tokens
                self.total_calls += 1
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error during research: {str(e)}"
    
    def get_remaining_credits(self) -> dict:
        """
        Attempt to fetch remaining credits from Perplexity API.
        
        Note: Perplexity API doesn't provide a direct credits endpoint,
        so we provide guidance for checking credits manually.
        
        Returns:
            Dict with credit info or guidance
        """
        try:
            # Try to get account info (experimental endpoint, may not exist)
            # This is a best-effort attempt
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "What is my current API credit balance?"
                    }
                ],
                max_tokens=100
            )
            
            # If we get here, try to extract credit info from response
            content = response.choices[0].message.content
            
            return {
                'status': 'info_received',
                'message': content
            }
        except Exception:
            # Perplexity doesn't have a direct credits endpoint
            # Return guidance for checking manually
            return {
                'status': 'manual_check_required',
                'message': 'Check your Perplexity API dashboard for remaining credits',
                'url': 'https://www.perplexity.ai/api/'
            }
    
    def get_usage_summary(self) -> dict:
        """Get usage summary for this session"""
        return {
            'total_calls': self.total_calls,
            'prompt_tokens': self.total_prompt_tokens,
            'completion_tokens': self.total_completion_tokens,
            'total_tokens': self.total_prompt_tokens + self.total_completion_tokens
        }


def create_research_agent():
    """
    Factory function to create a research agent using CrewAI
    """
    try:
        from crewai import Agent
        
        agent = Agent(
            role="Research Analyst",
            goal="Find relevant, up-to-date information on given topics",
            backstory="You are an expert researcher with access to the latest information. "
                     "Your task is to gather comprehensive, accurate data for article writing.",
            tools=[],  # Tools will be added dynamically
            verbose=True
        )
        return agent
    except ImportError:
        # Fallback if crewai not installed yet
        return None
