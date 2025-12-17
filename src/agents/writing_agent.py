"""
Writing Agent for crafting final article content.
"""


def create_writing_agent():
    """
    Factory function to create a writing agent using CrewAI
    """
    try:
        from crewai import Agent
        
        agent = Agent(
            role="Senior Writer",
            goal="Write engaging, professional LinkedIn articles",
            backstory="You are an award-winning writer specializing in professional content. "
                     "Your writing is clear, engaging, and tailored for LinkedIn audiences. "
                     "You know how to craft narratives that drive engagement and thoughtful discussion.",
            tools=[],
            verbose=True
        )
        return agent
    except ImportError:
        return None
