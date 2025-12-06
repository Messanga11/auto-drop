from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = False
    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/dropshipping"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Apify
    apify_api_token: Optional[str] = None
    
    # Creatify
    creatify_api_id: Optional[str] = None
    creatify_api_key: Optional[str] = None
    
    # Meta Ads
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    meta_access_token: Optional[str] = None
    meta_ad_account_id: Optional[str] = None
    meta_page_id: Optional[str] = None
    meta_pixel_id: Optional[str] = None
    
    # TikTok Ads
    tiktok_access_token: Optional[str] = None
    tiktok_advertiser_id: Optional[str] = None
    
    # WhatsApp
    whatsapp_access_token: Optional[str] = None
    whatsapp_phone_number_id: Optional[str] = None
    whatsapp_verify_token: Optional[str] = None
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    
    # Application
    secret_key: str = "change-me-in-production"
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        # Accepter SQLite pour développement ou PostgreSQL pour production
        if not v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite+aiosqlite://")):
            raise ValueError("DATABASE_URL must be PostgreSQL or SQLite connection string")
        return v

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v):
        if not v or not v.startswith("redis://"):
            raise ValueError("REDIS_URL must be a valid Redis connection string")
        return v


settings = Settings()

