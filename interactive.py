#!/usr/bin/env python
"""
Interactive article generation workflow with feedback loops.

Allows you to:
1. Generate research → review → edit
2. Generate plan → review → edit  
3. Generate article → review → edit

Usage:
    python interactive.py --topic "Your Article Topic" --skeleton "path/to/skeleton.md"
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

from src.config import Config, sanitize_topic
from src.visitor_agent import evaluate_article_from_all_personas, format_evaluations_for_markdown
from src.agents.research_agent import PerplexityResearchTool
from src.agents.verification_agent import VerificationAgent
from src.tasks.remarks_template import create_remarks_template


def load_file(filepath: str) -> str:
    """Load content from file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def save_file(content: str, filepath: str) -> str:
    """Save content to file"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath


def open_file_for_editing(filepath: str) -> bool:
    """
    Open file in VS Code for user to edit.
    Returns True if file was modified.
    """
    print(f"\nOpening file for editing: {filepath}")
    print("Editor: VS Code")
    print("=" * 60)
    
    # Get file modification time before
    mtime_before = os.path.getmtime(filepath) if os.path.exists(filepath) else 0
    
    # Open in VS Code and wait for it to close
    os.system(f"code --wait {filepath}")
    
    # Check if file was modified
    mtime_after = os.path.getmtime(filepath) if os.path.exists(filepath) else 0
    
    print("=" * 60)
    print("✓ File editing complete. Continuing...\n")
    return mtime_after > mtime_before


def prompt_yes_no(question: str) -> bool:
    """Prompt user for yes/no decision"""
    while True:
        response = input(f"\n{question} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def print_section(title: str, content: str, max_lines: int = 20):
    """Print a section with content preview"""
    lines = content.split('\n')
    print(f"\n{'='*60}")
    print(f"📄 {title}")
    print(f"{'='*60}")
    
    if len(lines) > max_lines:
        print('\n'.join(lines[:max_lines]))
        print(f"\n... ({len(lines) - max_lines} more lines)")
        print(f"\n(Full content: {len(content)} characters)")
    else:
        print(content)


def stage_1_research(topic: str, skeleton: str = None) -> dict:
    """Stage 1: Research with feedback loop"""
    print(f"\n{'='*60}")
    print("STAGE 1: RESEARCH")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    if skeleton:
        print(f"Skeleton: {skeleton}")
    
    output_dir = Config.get_topic_output_dir(topic)
    research_file = Path(output_dir) / "01_research.md"
    
    # Check if research already exists
    if research_file.exists():
        print(f"\n✓ Found existing research: {research_file}")
        if prompt_yes_no("Use existing research?"):
            content = load_file(research_file)
            return {'content': content, 'file': str(research_file), 'modified': False}
        print("Generating new research...")
    else:
        print("Generating research...")
    
    # Generate research
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
    save_file(research_content, research_file)
    
    print_section("Generated Research", research_content)
    
    # Feedback loop
    while True:
        if prompt_yes_no("\n✏️  Would you like to edit the research?"):
            open_file_for_editing(research_file)
            research_content = load_file(research_file)
            print_section("Updated Research", research_content)
        
        if prompt_yes_no("✓ Are you happy with the research?"):
            break
        
        if prompt_yes_no("Regenerate research with a different approach?"):
            research_query = input("Enter a new research prompt (or press Enter for default): ").strip()
            if not research_query:
                research_query = f"""Please provide comprehensive research on the topic: "{topic}" - try a different approach focusing on emerging trends and innovations."""
            
            research_content = research_tool.search(research_query)
            save_file(research_content, research_file)
            print_section("Regenerated Research", research_content)
        else:
            break
    
    return {'content': research_content, 'file': str(research_file), 'modified': True}


def stage_2_plan(topic: str, research: str, skeleton: str = None) -> dict:
    """Stage 2: Planning with feedback loop"""
    print(f"\n{'='*60}")
    print("STAGE 2: PLANNING")
    print(f"{'='*60}")
    
    output_dir = Config.get_topic_output_dir(topic)
    plan_file = Path(output_dir) / "02_plan.md"
    
    print("Generating article plan based on research...")
    
    research_tool = PerplexityResearchTool()
    skeleton_note = f"\n\nIncorporate these skeleton points:\n{skeleton}" if skeleton else ""
    
    planning_query = f"""Based on this research:
    {research[:1000]}...
    
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
    save_file(plan_content, plan_file)
    
    print_section("Generated Plan", plan_content)
    
    # Feedback loop
    while True:
        if prompt_yes_no("\n✏️  Would you like to edit the plan?"):
            open_file_for_editing(plan_file)
            plan_content = load_file(plan_file)
            print_section("Updated Plan", plan_content)
        
        if prompt_yes_no("✓ Are you happy with the plan?"):
            break
        
        if prompt_yes_no("Regenerate plan with different focus?"):
            focus = input("What should the plan focus on? (e.g., 'technical depth', 'practical examples', 'emotional impact'): ").strip()
            planning_query = f"""Based on this research:
            {research[:1000]}...
            
            Create a detailed article plan focused on {focus} for a LinkedIn post about: "{topic}"
            
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
            save_file(plan_content, plan_file)
            print_section("Regenerated Plan", plan_content)
        else:
            break
    
    return {'content': plan_content, 'file': str(plan_file), 'modified': True}


def stage_3_article(topic: str, research: str, plan: str) -> dict:
    """Stage 3: Writing with feedback loop"""
    print(f"\n{'='*60}")
    print("STAGE 3: WRITING")
    print(f"{'='*60}")
    
    output_dir = Config.get_topic_output_dir(topic)
    article_file = Path(output_dir) / "03_article.md"
    
    print("Generating article based on plan...")
    
    research_tool = PerplexityResearchTool()
    writing_query = f"""Write a professional LinkedIn article based on:
    
    Topic: {topic}
    
    Research findings:
    {research[:800]}...
    
    Article plan:
    {plan[:800]}...
    
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
    save_file(article_content, article_file)
    
    print_section("Generated Article", article_content)
    
    # Feedback loop with guaranteed remarks creation
    try:
        iteration = 1
        while True:
            if prompt_yes_no("\n✏️  Would you like to edit the article?"):
                open_file_for_editing(article_file)
                article_content = load_file(article_file)
                print_section("Updated Article", article_content)
            
            if prompt_yes_no("✓ Are you happy with the article?"):
                break
            
            if prompt_yes_no("Regenerate article with different style?"):
                style = input("Describe the desired style (e.g., 'more conversational', 'more data-driven', 'more storytelling'): ").strip()
                writing_query = f"""Rewrite this LinkedIn article with a {style} style:
                
                Topic: {topic}
                
                Current article:
                {article_content[:500]}...
                
                Plan:
                {plan[:500]}...
                
                Rewrite the complete article to be more {style} while maintaining all key points.
                The article should still be 800-1200 words and include hashtags."""
                
                article_content = research_tool.search(writing_query)
                save_file(article_content, article_file)
                iteration += 1
                print_section(f"Regenerated Article (Iteration {iteration})", article_content)
            else:
                break
    finally:
        # Create remarks file - guaranteed to run even if user cancels
        print("\n📝 Creating remarks template...")
        try:
            output_dir = Config.get_topic_output_dir(topic)
            remarks_file = Path(output_dir) / "remarks.md"
            remarks_content = create_remarks_template(topic)
            with open(remarks_file, 'w') as f:
                f.write(remarks_content)
            
            print(f"✓ Remarks template created: {remarks_file}")
        except Exception as e:
            print(f"⚠️  Error creating remarks file: {e}")
            import traceback
            traceback.print_exc()
    
    return {'content': article_content, 'file': str(article_file), 'modified': True}




def verify_article(topic: str, article_content: str) -> dict:
    """Verify statistics and find sources for article"""
    print(f"\n{'='*60}")
    print("🔍 VERIFY STATISTICS & SOURCES")
    print(f"{'='*60}")
    print("Extracting claims and finding sources...\n")
    
    verification_agent = VerificationAgent()
    verification_data = verification_agent.extract_and_verify_claims(article_content, topic)
    
    # Create sources file
    sources_content = verification_agent.format_sources_file(verification_data)
    output_dir = Config.get_topic_output_dir(topic)
    sources_file = Path(output_dir) / "sources.md"
    
    with open(sources_file, 'w') as f:
        f.write(sources_content)
    
    print(f"✓ Verification complete!")
    print(f"📋 Sources file created: {sources_file}")
    print(f"\nReview to:")
    print("  • Check verification status of each claim")
    print("  • Find sources and links for statistics")
    print("  • Add citations to your article")
    
    return {'sources_file': str(sources_file), 'verification': verification_data}


def main():
    parser = argparse.ArgumentParser(
        description="Interactive article generation with feedback loops"
    )
    parser.add_argument("--topic", required=True, help="The article topic")
    parser.add_argument("--skeleton", help="Optional path to article skeleton file")
    
    args = parser.parse_args()
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please set PERPLEXITY_API_KEY in .env file")
        sys.exit(1)
    
    # Load skeleton if provided
    skeleton_content = load_file(args.skeleton) if args.skeleton else None
    
    print(f"\n{'='*60}")
    print("LinkedIn Article Agent - Interactive Mode")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    # Stage 1: Research
    research_result = stage_1_research(args.topic, skeleton_content)
    research_content = research_result['content']
    
    # Stage 2: Planning
    plan_result = stage_2_plan(args.topic, research_content, skeleton_content)
    plan_content = plan_result['content']
    
    # Stage 3: Article
    article_result = stage_3_article(args.topic, research_content, plan_content)
    article_content = article_result['content']
    
    # Ask if user wants to verify sources
    if prompt_yes_no("\n🔍 Would you like to verify statistics and find sources?"):
        verify_article(args.topic, article_content)
    
    # Ask if user wants visitor feedback
    if prompt_yes_no("\n🤖 Would you like LinkedIn visitor reactions to your article?"):
        output_dir = Path(Config.get_topic_output_dir(args.topic))
        article_file = output_dir / "03_article.md"
        
        print(f"\nGenerating reactions from 3 personas...")
        lines = article_content.split('\n')
        article_title = lines[0].strip('# ').strip() if lines else "Article"
        
        evaluations = evaluate_article_from_all_personas(article_title, article_content, num_personas=3)
        
        # Display results
        print("\n" + "=" * 60)
        for eval in evaluations:
            stars = "⭐" * eval['score']
            print(f"\n{eval['persona']} {stars}")
            print(f"  → {eval['reaction']}")
            print(f"  💬 {eval['comment']}")
        print("\n" + "=" * 60)
        
        # Save reactions
        reactions_file = output_dir / "reactions.md"
        reactions_md = format_evaluations_for_markdown(evaluations)
        with open(reactions_file, 'w') as f:
            f.write(reactions_md)
        
        print(f"\n✓ Reactions saved: {reactions_file}\n")
    
    # Summary
    print(f"\n{'='*60}")
    print("✅ WORKFLOW COMPLETED")
    print(f"{'='*60}")
    print(f"\n📁 Outputs saved to: {Config.OUTPUTS_DIR}/")
    print(f"  1. Research:  03_research.md")
    print(f"  2. Plan:      02_plan.md")
    print(f"  3. Article:   03_article.md")
    print(f"\n✓ Your article is ready to post on LinkedIn!")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
