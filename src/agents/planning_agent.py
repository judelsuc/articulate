"""
Planning Agent for structuring article content.
"""


def create_planning_agent():
    """
    Factory function to create a planning agent using CrewAI
    """
    try:
        from crewai import Agent
        
        agent = Agent(
            role="Content Planner",
            goal="Create well-structured article plans that guide writing",
            backstory="You are an experienced content strategist who excels at organizing ideas "
                     "into compelling article structures. You understand what makes articles engaging "
                     "and how to structure information for LinkedIn audiences.",
            tools=[],
            verbose=True
        )
        return agent
    except ImportError:
        return None
