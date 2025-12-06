from pydantic import BaseModel, Field
from typing import Optional


class ScrapingStartRequest(BaseModel):
    facebook_max: int = Field(default=500, ge=1, le=1000, description="Max Facebook ads to scrape")
    tiktok_max: int = Field(default=500, ge=1, le=1000, description="Max TikTok pages to scrape")


class ScrapingStatusResponse(BaseModel):
    total_ads: int
    facebook_ads: int
    tiktok_ads: int


class ScrapingStartResponse(BaseModel):
    status: str
    message: str
    facebook_max: int
    tiktok_max: int

