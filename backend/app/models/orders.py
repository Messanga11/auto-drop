from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("scraped_ads.id"), nullable=False)
    product_name = Column(String(255))
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    address = Column(Text, nullable=False)
    city = Column(String(100))
    quantity = Column(Integer, default=1)
    status = Column(String(20), default='pending', index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    product = relationship("ScrapedAd", back_populates="orders")

