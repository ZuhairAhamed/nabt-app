"""
Configuration management for Nabt application.
"""

import os
from pathlib import Path
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        # API Keys
        self.groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
        
        # MongoDB Configuration
        self.mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.mongodb_database: str = os.getenv("MONGODB_DATABASE", "nabt")
        self.mongodb_collection: str = os.getenv("MONGODB_COLLECTION", "products")
        
        # Application Settings
        self.app_env: str = os.getenv("APP_ENV", "development")
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
        # API Settings
        self.api_host: str = os.getenv("API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        
        # Data Settings - use absolute path
        data_dir = os.getenv("DATA_DIRECTORY", "data")
        # If it's a relative path, make it absolute relative to project root
        if not os.path.isabs(data_dir):
            self.data_directory: str = str(PROJECT_ROOT / data_dir)
        else:
            self.data_directory: str = data_dir
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    """
    return Settings()

