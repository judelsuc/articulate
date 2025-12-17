import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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


# Ensure outputs directory exists
os.makedirs(Config.OUTPUTS_DIR, exist_ok=True)
