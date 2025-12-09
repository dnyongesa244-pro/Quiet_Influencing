#!/usr/bin/env python3
"""
Configuration loader for Social Media Collector
Simplified for YouTube testing
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration - Simplified for YouTube testing"""
    
    # YouTube API (Required for testing)
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    
    # Twitter API (Optional - will be used later)
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
    
    # Application settings
    DEFAULT_MAX_RESULTS = int(os.getenv('DEFAULT_MAX_RESULTS', '50'))  # Lower for testing
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'collected_data')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Rate limiting
    YOUTUBE_REQUEST_DELAY = float(os.getenv('YOUTUBE_REQUEST_DELAY', '0.2'))  # Slower for testing
    
    # Data preferences
    INCLUDE_REPLIES = os.getenv('INCLUDE_REPLIES', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls) -> Dict[str, str]:
        """
        Validate configuration and return any errors
        
        Returns:
            Dictionary of validation errors (empty if valid)
        """
        errors = {}
        
        # Check if .env file exists
        if not env_path.exists():
            print("⚠️  .env file not found. Create one from .env.example")
            print("   Or set YOUTUBE_API_KEY environment variable")
        
        # Check required YouTube API key
        if not cls.YOUTUBE_API_KEY:
            errors['youtube_api'] = "YouTube API key is not set"
            print("❌ YouTube API key is required for testing")
            print("   Set YOUTUBE_API_KEY in .env file")
        
        return errors
    
    @classmethod
    def print_config_summary(cls):
        """Print configuration summary for testing"""
        errors = cls.validate()
        
        print("\n" + "="*60)
        print("YOUTUBE TESTING CONFIGURATION")
        print("Twitter will be tested after YouTube verification")
        print("="*60)
        
        print(f"\nYouTube API Key: {'✓ SET' if cls.YOUTUBE_API_KEY else '❌ NOT SET'}")
        print(f"Default Max Results: {cls.DEFAULT_MAX_RESULTS}")
        print(f"Output Directory: {cls.OUTPUT_DIR}")
        print(f"Include Replies: {cls.INCLUDE_REPLIES}")
        print(f"Request Delay: {cls.YOUTUBE_REQUEST_DELAY}s")
        
        if errors:
            print(f"\n❌ CONFIGURATION ERRORS:")
            for key, error in errors.items():
                print(f"  • {error}")
            print("\nTo fix:")
            print("1. Create .env file from .env.example")
            print("2. Add your YouTube API key")
            print("3. Run: python youtube_collector.py python --max-comments 10")
        else:
            print(f"\n✅ Configuration looks good for YouTube testing!")
        
        print("="*60 + "\n")
    
    @classmethod
    def ensure_output_dir(cls):
        """Ensure output directory exists"""
        Path(cls.OUTPUT_DIR).mkdir(exist_ok=True, parents=True)
        return cls.OUTPUT_DIR


# Create a global config instance
config = Config()