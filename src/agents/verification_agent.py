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
        
        verification_query = f"""You are a fact-checker and researcher. Your job is to verify ALL statistics, percentages, numbers, and specific claims in this article.

For EACH claim you find:
1. Extract the exact claim
2. Research and verify it - find the actual source, link, or report
3. Provide the verification status:
   - ✓ VERIFIED with source link
   - ⚠️ LIKELY TRUE (widely accepted industry data)
   - ❓ CANNOT VERIFY (claim appears unsupported)
4. Provide the DIRECT source URL or exact reference where the claim comes from

DO NOT just tell the user "how to find it" - actually verify it yourself using your knowledge and internet searches.

Return results in structured markdown with:
- The exact claim
- Your verification status
- The source (with URL if possible)
- The publication date / year of the source
- A brief explanation of why you verified it that way

ARTICLE TO VERIFY:
{article_content}

Provide a comprehensive verification report for every statistic, percentage, and quantitative claim in the article."""
        
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
