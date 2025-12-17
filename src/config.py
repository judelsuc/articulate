import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def sanitize_topic(topic: str) -> str:
    """Convert topic to safe directory name"""
    # Convert to lowercase, replace spaces and special chars with hyphens
    safe_name = re.sub(r'[^\w\s-]', '', topic).strip()
    safe_name = re.sub(r'[-\s]+', '-', safe_name).lower()
    return safe_name or 'article'


class Config:
    """Application configuration"""
    
    # API Keys
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
    
    # Perplexity API Configuration (OpenAI-compatible endpoint)
    PERPLEXITY_API_URL = "https://api.perplexity.ai"
    PERPLEXITY_MODEL = "sonar-pro"
    
    # Output Configuration
    OUTPUTS_DIR = "outputs"
    
    # Timeout settings (in seconds)
    REQUEST_TIMEOUT = 60
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are set"""
        if not cls.PERPLEXITY_API_KEY:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    @classmethod
    def get_topic_output_dir(cls, topic: str) -> str:
        """Get output directory for a specific topic"""
        safe_topic = sanitize_topic(topic)
        output_dir = os.path.join(cls.OUTPUTS_DIR, safe_topic)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir


# Ensure outputs directory exists
os.makedirs(Config.OUTPUTS_DIR, exist_ok=True)
