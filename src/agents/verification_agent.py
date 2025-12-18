"""
Verification Agent for checking statistics, claims, and finding sources.
"""
from src.agents.research_agent import PerplexityResearchTool


class VerificationAgent:
    """Agent for verifying claims, statistics, and finding sources"""
    
    def __init__(self):
        self.research_tool = PerplexityResearchTool()
    
    def extract_and_verify_claims(self, article_content: str, topic: str) -> dict:
        """
        Extract claims and statistics from article and verify them with sources
        
        Args:
            article_content: The full article text
            topic: Article topic for context
            
        Returns:
            Dictionary with extracted claims and verification results
        """
        
        verification_query = f"""Analyze this LinkedIn article about "{topic}" and:

1. Extract ALL statistics, percentages, numbers, and specific claims (e.g., "40% adoption", "2023 data", "Apple reported")
2. For each claim, provide:
   - The exact claim from the article
   - Verification status: ✓ VERIFIED, ⚠️ LIKELY (common knowledge), or ❓ NEEDS REVIEW
   - Suggested source or reference
   - Direct link (if available) or how to find it

Format as a structured list.

ARTICLE:
{article_content}

Provide the verification results in clear markdown format with sections for each claim."""
        
        verification_content = self.research_tool.search(verification_query)
        
        return {
            'verification': verification_content,
            'topic': topic
        }
    
    def format_sources_file(self, verification_data: dict) -> str:
        """Format verification results into a sources.md file"""
        
        sources_content = f"""# Sources & Verification: {verification_data['topic']}

## Statistics & Claims Verification

Below are all the key statistics, percentages, and claims extracted from the article, along with verification status and sources.

---

{verification_data['verification']}

---

## How to Use This File

✓ **VERIFIED** = Confirmed accurate, source linked
⚠️ **LIKELY** = Common industry knowledge, generally accepted
❓ **NEEDS REVIEW** = Could not find immediate source, should fact-check before publishing

## Next Steps

1. Review each claim marked with ❓ 
2. Use the suggested sources to verify or find better references
3. Add direct links to your article using [text](url) format
4. Update this file as you find more sources
5. Once all claims are verified, your article is ready to post!

---

*Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return sources_content
