"""
Tasks for the article generation workflow.
"""
from typing import Optional


def create_research_task(agent, topic: str) -> dict:
    """Create a research task for gathering information"""
    return {
        "description": f"""Research and gather comprehensive information about: {topic}
        
        Find:
        - Current trends and statistics
        - Expert opinions and insights
        - Recent developments
        - Relevant case studies or examples
        - Key considerations and challenges""",
        "expected_output": "A comprehensive research report with cited sources and key findings",
        "agent": agent
    }


def create_planning_task(agent, topic: str, skeleton: Optional[str] = None) -> dict:
    """Create a planning task for structuring the article"""
    skeleton_note = f"\n\nConsider this provided skeleton:\n{skeleton}" if skeleton else ""
    
    return {
        "description": f"""Create a detailed article plan for: {topic}
        
        The plan should include:
        - Compelling headline
        - Hook/opening statement
        - 3-5 main sections with subpoints
        - Key statistics or data points to include
        - Call-to-action for ending
        - Hashtags and LinkedIn engagement tips{skeleton_note}""",
        "expected_output": "A structured Markdown file with complete article outline and writing guidelines",
        "agent": agent
    }


def create_writing_task(agent, topic: str, research: str, plan: str) -> dict:
    """Create a writing task for generating the final article"""
    return {
        "description": f"""Write a professional LinkedIn article about: {topic}
        
        Use this research: {research[:500]}...
        Follow this plan: {plan[:500]}...
        
        Guidelines:
        - Target audience: LinkedIn professionals and industry leaders
        - Tone: Professional yet conversational
        - Length: 800-1200 words
        - Include 2-3 relevant statistics
        - Use short paragraphs for readability
        - Include a strong call-to-action
        - Optimize for LinkedIn algorithm (engagement, shares)""",
        "expected_output": "A complete, polished LinkedIn article ready for posting",
        "agent": agent
    }
