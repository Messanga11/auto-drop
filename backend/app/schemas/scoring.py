from pydantic import BaseModel, Field
from typing import List, Optional


class TopProductResponse(BaseModel):
    product_id: int
    platform: str
    score: float
    ad_url: Optional[str] = None
    page_name: Optional[str] = None
    caption: Optional[str] = None


class ScoringCalculateResponse(BaseModel):
    status: str
    top_5_products: List[TopProductResponse]
    message: str

