#!/usr/bin/env python
"""
File-based workflow for article generation with manual iteration.

This script generates each stage and saves to files you can edit.

Usage:
    # Stage 1: Generate research
    python workflow.py --topic "Your Topic" --stage research
    
    # Edit outputs/research.md as needed
    
    # Stage 2: Generate plan based on research
    python workflow.py --topic "Your Topic" --stage plan
    
    # Edit outputs/plan.md as needed
    
    # Stage 3: Generate article
    python workflow.py --topic "Your Topic" --stage article
    
    # Edit outputs/article.md as needed

Or run all stages at once:
    python workflow.py --topic "Your Topic" --all
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from src.config import Config
from src.agents.research_agent import PerplexityResearchTool


def load_file(filepath: str) -> str:
    """Load content from file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None


def save_file(content: str, filepath: str, overwrite: bool = False) -> str:
    """Save content to file with optional overwrite protection"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    if Path(filepath).exists() and not overwrite:
        print(f"\n⚠️  File already exists: {filepath}")
        if input("Overwrite? (y/n): ").strip().lower() != 'y':
            print("Skipped. Edit the file manually and run the next stage.")
            return filepath
    
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✓ Saved: {filepath}")
    return filepath


def stage_research(topic: str, skeleton: str = None, force: bool = False) -> str:
    """Generate research"""
    print(f"\n{'='*60}")
    print("🔍 STAGE 1: RESEARCH")
    print(f"{'='*60}")
    print(f"Topic: {topic}\n")
    
    research_file = Path(Config.OUTPUTS_DIR) / "research.md"
    
    if research_file.exists() and not force:
        print(f"✓ Found existing research: {research_file}")
        print("Tip: Edit this file, then run stage 2 (plan)")
        return str(research_file)
    
    print("Generating research from Perplexity API...")
    
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
    
    if research_content.startswith("Error"):
        print(f"❌ {research_content}")
        sys.exit(1)
    
    save_file(research_content, research_file, overwrite=force)
    
    print(f"\n📝 Research generated ({len(research_content)} characters)")
    print(f"📋 Next step: Review and edit {research_file}")
    print(f"   Then run: python workflow.py --topic \"{topic}\" --stage plan")
    
    return str(research_file)


def stage_plan(topic: str, skeleton: str = None, force: bool = False) -> str:
    """Generate plan based on research"""
    print(f"\n{'='*60}")
    print("📋 STAGE 2: PLANNING")
    print(f"{'='*60}")
    print(f"Topic: {topic}\n")
    
    research_file = Path(Config.OUTPUTS_DIR) / "research.md"
    plan_file = Path(Config.OUTPUTS_DIR) / "plan.md"
    
    # Load research
    research_content = load_file(research_file)
    if not research_content:
        print(f"❌ Research not found. Run stage 1 first:")
        print(f"   python workflow.py --topic \"{topic}\" --stage research")
        sys.exit(1)
    
    if plan_file.exists() and not force:
        print(f"✓ Found existing plan: {plan_file}")
        print("Tip: Edit this file, then run stage 3 (article)")
        return str(plan_file)
    
    print("Generating article plan based on research...")
    
    research_tool = PerplexityResearchTool()
    skeleton_note = f"\n\nIncorporate these skeleton points:\n{skeleton}" if skeleton else ""
    
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
    {skeleton_note}
    
    Format as Markdown with clear structure."""
    
    plan_content = research_tool.search(planning_query)
    
    if plan_content.startswith("Error"):
        print(f"❌ {plan_content}")
        sys.exit(1)
    
    save_file(plan_content, plan_file, overwrite=force)
    
    print(f"\n📝 Plan generated ({len(plan_content)} characters)")
    print(f"📋 Next step: Review and edit {plan_file}")
    print(f"   Then run: python workflow.py --topic \"{topic}\" --stage article")
    
    return str(plan_file)


def stage_article(topic: str, force: bool = False) -> str:
    """Generate article based on plan"""
    print(f"\n{'='*60}")
    print("✍️  STAGE 3: WRITING ARTICLE")
    print(f"{'='*60}")
    print(f"Topic: {topic}\n")
    
    research_file = Path(Config.OUTPUTS_DIR) / "research.md"
    plan_file = Path(Config.OUTPUTS_DIR) / "plan.md"
    article_file = Path(Config.OUTPUTS_DIR) / "article.md"
    
    # Load dependencies
    research_content = load_file(research_file)
    plan_content = load_file(plan_file)
    
    if not research_content:
        print(f"❌ Research not found. Run stage 1 first.")
        sys.exit(1)
    
    if not plan_content:
        print(f"❌ Plan not found. Run stage 2 first.")
        sys.exit(1)
    
    if article_file.exists() and not force:
        print(f"✓ Found existing article: {article_file}")
        print("Tip: Edit this file or run with --force to regenerate")
        return str(article_file)
    
    print("Generating article based on plan...")
    
    research_tool = PerplexityResearchTool()
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
    
    if article_content.startswith("Error"):
        print(f"❌ {article_content}")
        sys.exit(1)
    
    save_file(article_content, article_file, overwrite=force)
    
    print(f"\n📝 Article generated ({len(article_content)} characters)")
    print(f"🎉 Your article is ready!")
    print(f"📁 Location: {article_file}")
    print(f"\n📋 Next steps:")
    print(f"   1. Review and edit {article_file}")
    print(f"   2. Copy to LinkedIn")
    print(f"   3. Publish!")
    
    return str(article_file)


def main():
    parser = argparse.ArgumentParser(
        description="File-based article generation workflow"
    )
    parser.add_argument("--topic", required=True, help="Article topic")
    parser.add_argument("--skeleton", help="Path to article skeleton file")
    parser.add_argument(
        "--stage",
        choices=['research', 'plan', 'article'],
        help="Which stage to run"
    )
    parser.add_argument("--all", action="store_true", help="Run all stages")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Set PERPLEXITY_API_KEY in .env file")
        sys.exit(1)
    
    # Load skeleton if provided
    skeleton_content = None
    if args.skeleton:
        skeleton_content = load_file(args.skeleton)
        if not skeleton_content:
            sys.exit(1)
    
    print(f"\n{'='*60}")
    print("📄 LinkedIn Article Generator - Workflow Mode")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Run stages
    if args.all or not args.stage:
        stage_research(args.topic, skeleton_content, args.force)
        stage_plan(args.topic, skeleton_content, args.force)
        stage_article(args.topic, args.force)
    elif args.stage == 'research':
        stage_research(args.topic, skeleton_content, args.force)
    elif args.stage == 'plan':
        stage_plan(args.topic, skeleton_content, args.force)
    elif args.stage == 'article':
        stage_article(args.topic, args.force)
    
    print(f"\n{'='*60}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
