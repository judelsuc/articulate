#!/usr/bin/env python
"""
Evaluate generated articles with LinkedIn visitor personas.

Usage:
    python visitor.py outputs/your-topic/article.md
    python visitor.py --topic "Your Topic"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from src.config import Config
from src.visitor_agent import evaluate_article_from_all_personas, format_evaluations_for_markdown


def load_article(filepath: str) -> tuple:
    """Load article and extract title"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract title from first markdown heading
        lines = content.split('\n')
        title = lines[0].strip('# ').strip() if lines else "Untitled"
        
        return title, content
    except FileNotFoundError:
        print(f"Error: Article not found at {filepath}")
        return None, None


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate LinkedIn articles with persona-based feedback"
    )
    parser.add_argument(
        "article_path",
        nargs='?',
        help="Path to article.md file"
    )
    parser.add_argument(
        "--topic",
        help="Topic name (uses outputs/topic/article.md)"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=3,
        help="Number of personas to generate (1-5, default 3)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save reactions to file (default: reactions.md in same directory)"
    )
    
    args = parser.parse_args()
    
    # Determine article path
    if args.topic:
        from src.config import sanitize_topic
        safe_topic = sanitize_topic(args.topic)
        article_path = f"outputs/{safe_topic}/article.md"
    elif args.article_path:
        article_path = args.article_path
    else:
        parser.print_help()
        sys.exit(1)
    
    # Load article
    title, content = load_article(article_path)
    if not content:
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("🤖 LinkedIn Visitor Agent - Evaluating Article")
    print(f"{'='*60}")
    print(f"Article: {title}")
    print(f"Path: {article_path}")
    print(f"Personas: {args.num}")
    print(f"\nGenerating reactions...\n")
    
    # Generate evaluations
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    
    evaluations = evaluate_article_from_all_personas(title, content, args.num)
    
    # Display results
    print("=" * 60)
    for eval in evaluations:
        stars = "⭐" * eval['score']
        print(f"\n{eval['persona']} {stars}")
        print(f"  Reaction: {eval['reaction']}")
        print(f"  Comment: {eval['comment']}")
    print(f"\n{'='*60}\n")
    
    # Save reactions
    reactions_md = format_evaluations_for_markdown(evaluations)
    
    if args.output:
        output_file = args.output
    else:
        # Default: save in same directory as article
        output_dir = Path(article_path).parent
        output_file = str(output_dir / "reactions.md")
    
    with open(output_file, 'w') as f:
        f.write(reactions_md)
    
    print(f"✓ Reactions saved to: {output_file}\n")


if __name__ == "__main__":
    main()
