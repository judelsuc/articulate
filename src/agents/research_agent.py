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
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error during research: {str(e)}"


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
