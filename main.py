#!/usr/bin/env python
"""
Main entry point for the LinkedIn Article Agent workflow.

Usage:
    python main.py --topic "Your Article Topic" --skeleton "path/to/skeleton.md"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from src.config import Config
from src.agents.research_agent import PerplexityResearchTool
from src.tasks.article_tasks import (
    create_research_task,
    create_planning_task,
    create_writing_task
)


def load_skeleton(skeleton_path: str) -> str:
    """Load article skeleton from file"""
    if not skeleton_path:
        return None
    
    try:
        with open(skeleton_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Skeleton file not found at {skeleton_path}")
        return None


def save_output(content: str, filename: str, topic: str) -> str:
    """Save generated content to topic-specific output directory"""
    output_dir = Config.get_topic_output_dir(topic)
    output_path = Path(output_dir) / filename
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    return str(output_path)


def run_workflow(topic: str, skeleton: str = None) -> dict:
    """
    Run the complete article generation workflow
    
    Args:
        topic: The article topic
        skeleton: Optional path to article skeleton file
        
    Returns:
        Dictionary with research, plan, and article outputs
    """
    print(f"\n{'='*60}")
    print(f"LinkedIn Article Agent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set PERPLEXITY_API_KEY and OPENAI_API_KEY in .env file")
        sys.exit(1)
    
    # Load skeleton if provided
    skeleton_content = load_skeleton(skeleton) if skeleton else None
    
    results = {}
    
    # Step 1: Research
    print("Step 1: Researching topic...")
    print("-" * 40)
    research_tool = PerplexityResearchTool()
    research_query = f"""Please provide comprehensive research on the topic: "{topic}"
    
    Include:
    - Current trends and statistics
    - Expert perspectives
    - Recent developments
    - Practical applications
    - Challenges and considerations
    
    Format the response for use in a professional LinkedIn article."""
    
    research_content = research_tool.search(research_query)
    print("Research completed!")
    print(f"Research length: {len(research_content)} characters\n")
    
    # Save research
    research_file = save_output(research_content, "research.md", args.topic)
    results['research'] = research_content
    results['research_file'] = research_file
    
    # Step 2: Planning
    print("Step 2: Creating article plan...")
    print("-" * 40)
    
    planning_query = f"""Based on this research:
    {research_content[:1000]}...
    
    Create a detailed article plan for a LinkedIn post about: "{topic}"
    
    The plan should include:
    - Compelling headline options
    - Hook/opening statement
    - 3-5 main sections with key points
    - Supporting statistics to include
    - Strong closing and call-to-action
    - Suggested hashtags
    
    {'Incorporate these skeleton points:\\n' + skeleton_content if skeleton_content else ''}
    
    Format as Markdown with clear structure."""
    
    plan_content = research_tool.search(planning_query)
    print("Plan created!")
    print(f"Plan length: {len(plan_content)} characters\n")
    
    # Save plan
    plan_file = save_output(plan_content, "plan.md", args.topic)
    results['plan'] = plan_content
    results['plan_file'] = plan_file
    
    # Step 3: Writing
    print("Step 3: Writing article...")
    print("-" * 40)
    
    writing_query = f"""Write a professional LinkedIn article based on:
    
    Topic: {topic}
    
    Research findings:
    {research_content[:800]}...
    
    Article plan:
    {plan_content[:800]}...
    
    Create a complete, engaging LinkedIn article that:
    - Starts with a compelling hook
    - Is 800-1200 words
    - Follows the provided plan structure
    - Includes relevant data points and examples
    - Has a strong call-to-action at the end
    - Uses short paragraphs for readability
    - Is professional yet conversational
    - Ends with relevant hashtags
    
    Write the complete article ready to post on LinkedIn."""
    
    article_content = research_tool.search(writing_query)
    print("Article written!")
    print(f"Article length: {len(article_content)} characters\n")
    
    # Save article
    article_file = save_output(article_content, "article.md", args.topic)
    results['article'] = article_content
    results['article_file'] = article_file
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate LinkedIn articles using AI agents and web research"
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="The article topic"
    )
    parser.add_argument(
        "--skeleton",
        help="Optional path to article skeleton file"
    )
    
    args = parser.parse_args()
    
    # Run workflow
    results = run_workflow(args.topic, args.skeleton)
    
    # Print summary
    print("\n" + "="*60)
    print("WORKFLOW COMPLETED")
    print("="*60)
    print(f"\n✓ Research: {results['research_file']}")
    print(f"✓ Plan:     {results['plan_file']}")
    print(f"✓ Article:  {results['article_file']}")
    print("\nAll outputs saved to the 'outputs' directory.")
    print("\nNext steps:")
    print("1. Review the plan in 'outputs/plan.md'")
    print("2. Review the article in 'outputs/article.md'")
    print("3. Make any edits as needed")
    print("4. Post to LinkedIn!\n")


if __name__ == "__main__":
    main()
