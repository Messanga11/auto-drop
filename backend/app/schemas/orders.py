from pydantic import BaseModel, Field
from typing import Optional


class OrderCreateRequest(BaseModel):
    productId: int = Field(..., description="Product ID")
    productName: Optional[str] = None
    fullName: str = Field(..., min_length=2, max_length=255)
    phone: str = Field(..., pattern=r"^\+?[0-9]{10,15}$")
    address: str = Field(..., min_length=10)
    city: str = Field(..., min_length=2, max_length=100)
    quantity: int = Field(default=1, ge=1, le=10)


class OrderResponse(BaseModel):
    id: int
    orderId: int
    message: str

