"""
LinkedIn Visitor Agent - Evaluates articles from different personas.
"""
import random
from openai import OpenAI
from src.config import Config


class LinkedInVisitor:
    """Represents a LinkedIn visitor with a specific persona"""
    
    def __init__(self, persona: str, background: str, focus_areas: list, style: str):
        self.persona = persona
        self.background = background
        self.focus_areas = focus_areas
        self.style = style
        self.client = OpenAI(
            api_key=Config.PERPLEXITY_API_KEY,
            base_url=Config.PERPLEXITY_API_URL
        )
    
    def evaluate_article(self, article_title: str, article_content: str) -> dict:
        """
        Evaluate the article and generate reaction + comment.
        
        Returns:
            {
                'persona': 'CxO',
                'score': 4,
                'reaction': 'Great insight',
                'comment': 'This strategic framing...'
            }
        """
        prompt = f"""You are a LinkedIn user with this profile:
        
Persona: {self.persona}
Background: {self.background}
Focus Areas: {', '.join(self.focus_areas)}
Communication Style: {self.style}

An article was posted:
Title: {article_title}

Content (excerpt):
{article_content[:1000]}...

Your task: Evaluate this article from YOUR perspective.

Return a JSON response with:
{{
    "score": <1-5 integer>,
    "reaction": "<one of: Great insight, Boring, Already seen, Don't care, Mixed>",
    "comment": "<1-2 sentences, short, staying in character, funny if appropriate>"
}}

Keep the comment SHORT - max 2 sentences. Make it authentic to your persona.
If the reaction is "Boring", make a sarcastic comment.
If "Already seen", reference what you've heard before.
If "Great insight", be specific about what resonates.

Return ONLY valid JSON, no markdown or extra text."""
        
        try:
            response = self.client.chat.completions.create(
                model=Config.PERPLEXITY_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            result = json.loads(response_text)
            result['persona'] = self.persona
            return result
            
        except Exception as e:
            # Fallback response
            return {
                'persona': self.persona,
                'score': 3,
                'reaction': 'Mixed',
                'comment': f'Interesting perspective from a {self.persona} standpoint.'
            }


# Define all personas
PERSONAS = {
    'CxO': LinkedInVisitor(
        persona='CxO (Chief Executive)',
        background='VP/C-Suite leader, 15+ years enterprise experience',
        focus_areas=['Business value', 'ROI', 'Strategic implications', 'Market impact'],
        style='Strategic, high-level, business-focused, sometimes dismissive of tactics'
    ),
    'Engineer': LinkedInVisitor(
        persona='Senior Engineer',
        background='Software engineer, 10+ years, deep technical background',
        focus_areas=['Technical depth', 'Implementation', 'Architecture', 'Code quality'],
        style='Technical, detailed, asks implementation questions, references best practices'
    ),
    'Non-Technical': LinkedInVisitor(
        persona='Non-Technical Professional',
        background='Marketing/Operations background, limited technical knowledge',
        focus_areas=['Practical application', 'Clarity', 'Real-world impact', 'Relatable examples'],
        style='Accessible, sometimes confused by jargon, asks clarifying questions'
    ),
    'Marketer': LinkedInVisitor(
        persona='Marketing Manager',
        background='5+ years in marketing, focused on brand and messaging',
        focus_areas=['Brand messaging', 'Audience engagement', 'Storytelling', 'Market trends'],
        style='Narrative-focused, engagement-oriented, trend-aware, sometimes superficial'
    ),
    'Product Manager': LinkedInVisitor(
        persona='Product Manager',
        background='Product leadership, user-centric mindset',
        focus_areas=['User needs', 'Product strategy', 'Use cases', 'Feature implications'],
        style='User-focused, strategic, asks "why", connects to product decisions'
    )
}


def evaluate_article_from_all_personas(article_title: str, article_content: str, num_personas: int = 3) -> list:
    """
    Get evaluations from randomly selected personas.
    
    Args:
        article_title: Title of the article
        article_content: Full article content
        num_personas: Number of personas to evaluate (default 3)
    
    Returns:
        List of evaluation dictionaries
    """
    selected_personas = random.sample(list(PERSONAS.keys()), min(num_personas, len(PERSONAS)))
    evaluations = []
    
    for persona_name in selected_personas:
        visitor = PERSONAS[persona_name]
        evaluation = visitor.evaluate_article(article_title, article_content)
        evaluations.append(evaluation)
    
    return sorted(evaluations, key=lambda x: x['score'], reverse=True)


def format_evaluations_for_display(evaluations: list) -> str:
    """Format evaluations for nice display"""
    output = "# LinkedIn Visitor Reactions\n\n"
    
    for eval in evaluations:
        stars = "⭐" * eval['score'] + "☆" * (5 - eval['score'])
        output += f"## {eval['persona']}\n"
        output += f"**Score:** {stars} ({eval['score']}/5)\n"
        output += f"**Reaction:** {eval['reaction']}\n"
        output += f"**Comment:** {eval['comment']}\n\n"
    
    return output


def format_evaluations_for_markdown(evaluations: list) -> str:
    """Format evaluations as clean markdown"""
    output = "# 💬 LinkedIn Visitor Reactions\n\n"
    output += f"**{len(evaluations)} personas evaluated this article:**\n\n"
    
    for eval in evaluations:
        stars = "⭐" * eval['score']
        output += f"### {eval['persona']} {stars}\n"
        output += f"> **{eval['reaction']}**\n\n"
        output += f"> {eval['comment']}\n\n"
    
    return output
