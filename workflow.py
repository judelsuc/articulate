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

from src.config import Config, sanitize_topic
from src.visitor_agent import evaluate_article_from_all_personas, format_evaluations_for_markdown
from src.agents.research_agent import PerplexityResearchTool
from src.tasks.remarks_template import create_remarks_template


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
    
    output_dir = Config.get_topic_output_dir(topic)
    research_file = Path(output_dir) / "01_research.md"
    
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
    
    output_dir = Config.get_topic_output_dir(topic)
    research_file = Path(output_dir) / "01_research.md"
    plan_file = Path(output_dir) / "02_plan.md"
    
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
    
    output_dir = Config.get_topic_output_dir(topic)
    research_file = Path(output_dir) / "01_research.md"
    plan_file = Path(output_dir) / "02_plan.md"
    article_file = Path(output_dir) / "03_article.md"
    
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
    
    # Create remarks file
    output_dir = Config.get_topic_output_dir(topic)
    remarks_file = Path(output_dir) / "remarks.md"
    remarks_content = create_remarks_template(topic)
    save_file(remarks_content, remarks_file, overwrite=force)
    
    print(f"\n📝 Article generated ({len(article_content)} characters)")
    print(f"📝 Remarks template created for your feedback")
    print(f"\n📁 Files created:")
    print(f"   • {article_file}")
    print(f"   • {remarks_file}")
    print(f"\n📋 Next steps:")
    print(f"   1. Add your remarks and feedback to {remarks_file}")
    print(f"   2. Review and polish {article_file}")
    print(f"   3. Post to LinkedIn!")
    
    return str(article_file)


def stage_revise(topic: str, force: bool = False) -> str:
    """Revise article based on remarks feedback"""
    print(f"\n{'='*60}")
    print("✏️  STAGE 3B: REVISE BASED ON REMARKS")
    print(f"{'='*60}")
    print(f"Topic: {topic}\n")
    
    output_dir = Config.get_topic_output_dir(topic)
    article_file = Path(output_dir) / "03_article.md"
    remarks_file = Path(output_dir) / "remarks.md"
    revised_file = Path(output_dir) / "04_article_revised.md"
    
    # Load article and remarks
    article_content = load_file(article_file)
    remarks_content = load_file(remarks_file)
    
    if not article_content:
        print(f"❌ Article not found. Run stage 3 first.")
        sys.exit(1)
    
    if not remarks_content:
        print(f"⚠️  Remarks file not found. Create one at {remarks_file}")
        print("Using empty remarks for revision context.")
        remarks_content = "No specific feedback provided."
    
    print("Revising article based on your feedback...")
    
    research_tool = PerplexityResearchTool()
    revision_query = f"""You are a professional editor revising a LinkedIn article.

Here is the CURRENT article:
{article_content}

---

Here is the AUTHOR'S FEEDBACK and REMARKS:
{remarks_content}

---

Please revise the article to incorporate the author's feedback while:
- Maintaining the same structure and flow
- Keeping the professional tone
- Preserving all key points and data
- Addressing specific concerns raised in the remarks
- Improving clarity and impact based on the feedback
- Keeping it suitable for LinkedIn (800-1200 words)

Output the complete revised article, ready to post."""
    
    revised_content = research_tool.search(revision_query)
    
    if revised_content.startswith("Error"):
        print(f"❌ {revised_content}")
        sys.exit(1)
    
    save_file(revised_content, revised_file, overwrite=force)
    
    print(f"\n📝 Article revised ({len(revised_content)} characters)")
    print(f"📋 Revised article saved: {revised_file}")
    print(f"   Compare with original: {article_file}")
    print(f"   Then run: python workflow.py --topic \"{topic}\" --stage article --force")
    
    return str(revised_file)


def stage_visitor_feedback(topic: str, article_path: str) -> str:
    """Stage 4: Get visitor feedback on article"""
    print(f"\n{'='*60}")
    print("🤖 STAGE 4: VISITOR FEEDBACK")
    print(f"{'='*60}\n")
    
    # Load article
    try:
        with open(article_path, 'r') as f:
            article_content = f.read()
        
        lines = article_content.split('\n')
        article_title = lines[0].strip('# ').strip() if lines else "Article"
    except FileNotFoundError:
        print(f"Error: Article not found at {article_path}")
        return None
    
    print("Generating LinkedIn visitor reactions...")
    print("(3 random personas: CxO, Engineer, Non-Technical, Marketer, Product Manager)\n")
    
    # Generate evaluations
    evaluations = evaluate_article_from_all_personas(article_title, article_content, num_personas=3)
    
    # Display results
    for eval in evaluations:
        stars = "⭐" * eval['score']
        print(f"{eval['persona']} {stars}")
        print(f"  → {eval['reaction']}")
        print(f"  💬 {eval['comment']}\n")
    
    # Save reactions
    output_dir = Path(article_path).parent
    reactions_file = output_dir / "reactions.md"
    reactions_md = format_evaluations_for_markdown(evaluations)
    
    with open(reactions_file, 'w') as f:
        f.write(reactions_md)
    
    print(f"✓ Reactions saved: {reactions_file}\n")
    
    return str(reactions_file)


def main():
    parser = argparse.ArgumentParser(
        description="File-based article generation workflow"
    )
    parser.add_argument("--topic", required=True, help="Article topic")
    parser.add_argument("--skeleton", help="Path to article skeleton file")
    parser.add_argument(
        "--stage",
        choices=['research', 'plan', 'article', 'revise'],
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
        article_file = stage_article(args.topic, args.force)
        
        # Ask if user wants visitor feedback
        print(f"\n{'='*60}")
        print("Would you like LinkedIn visitor reactions to your article?")
        print("(3 personas will evaluate: CxO, Engineer, Non-Tech, Marketer, PM)")
        if input("Generate visitor feedback? (y/n): ").strip().lower() == 'y':
            stage_visitor_feedback(args.topic, article_file)
    elif args.stage == 'research':
        stage_research(args.topic, skeleton_content, args.force)
    elif args.stage == 'plan':
        stage_plan(args.topic, skeleton_content, args.force)
    elif args.stage == 'article':
        article_file = stage_article(args.topic, args.force)
        
        # Ask if user wants visitor feedback
        print(f"\n{'='*60}")
        print("Would you like LinkedIn visitor reactions to your article?")
        if input("Generate visitor feedback? (y/n): ").strip().lower() == 'y':
            stage_visitor_feedback(args.topic, article_file)
    elif args.stage == 'revise':
        stage_revise(args.topic, args.force)
    
    print(f"\n{'='*60}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
