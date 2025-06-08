from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):
    """Application settings."""
    
    # VQA adapter settings
    vqa_adapter: str = "vlm"  # Default to use VLM
    lms_api: str = 'http://some_free_VLM_api:1234/v1' # Default value (Actual is in `.env`)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

CONFIG = AppConfig()