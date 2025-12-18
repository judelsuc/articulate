#!/usr/bin/env python
"""
Quick demo of API usage tracking functionality.
This shows how the usage accumulates across multiple API calls.
"""

from src.agents.research_agent import PerplexityResearchTool

def demo_usage_tracking():
    """Demonstrate the usage tracking feature"""
    print("=" * 60)
    print("API USAGE TRACKING DEMO")
    print("=" * 60)
    
    # Create research tool
    tool = PerplexityResearchTool()
    
    print("\n✓ Research tool created")
    print(f"  - Initial state: {tool.get_usage_summary()}")
    
    # Simulate multiple API calls
    print("\n📝 Simulating API calls...")
    print("  (In real usage, these would be research, planning, writing)")
    
    # Show what usage tracking looks like after calls
    print("\n✓ After API calls complete, you'll see:")
    
    # This would show the actual values after running the workflow
    print("\n" + "=" * 60)
    print("📊 API USAGE SUMMARY (Example)")
    print("=" * 60)
    print("API Calls: 5")
    print("Prompt Tokens: 3,456")
    print("Completion Tokens: 8,934")
    print("Total Tokens: 12,390")
    print("\n💡 Tip: Check your Perplexity API dashboard for remaining credits")
    print("   https://www.perplexity.ai/api/")
    print("=" * 60)
    
    print("\n📌 How to use:")
    print("  1. workflow.py --topic 'Your Topic' --all")
    print("     → Runs all stages and shows usage at the end")
    print("\n  2. interactive.py --topic 'Your Topic'")
    print("     → Interactive mode with usage shown at completion")
    print("\n  3. Check the API_USAGE_TRACKING.md file for details")

if __name__ == "__main__":
    demo_usage_tracking()
