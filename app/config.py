from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # API Configuration
    API_KEY: str = os.getenv("API_KEY", "")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    # Redis Configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Job Configuration
    JOB_TIMEOUT: int = 300  # 5 minutes
    JOB_RETRIES: int = 3
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
