from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ScrapedAd(Base):
    __tablename__ = "scraped_ads"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(20), nullable=False, index=True)  # facebook, tiktok
    ad_id = Column(String(255), unique=True)
    ad_snapshot_url = Column(Text)
    video_url = Column(Text)
    page_name = Column(String(255))
    advertiser_name = Column(String(255))
    caption = Column(Text)
    ad_creative_bodies = Column(Text)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    impressions_upper_bound = Column(Integer)
    ad_delivery_start_time = Column(DateTime)
    first_shown_date = Column(DateTime)
    scraped_at = Column(DateTime, server_default=func.now())
    scored = Column(Boolean, default=False, index=True)
    selected_for_campaign = Column(Boolean, default=False)

    # Relationships (lazy imports to avoid circular dependencies)
    product_score = relationship("ProductScore", back_populates="ad", uselist=False)
    creatives = relationship("Creative", back_populates="product", lazy="select")
    campaigns = relationship("Campaign", back_populates="product", lazy="select")
    orders = relationship("Order", back_populates="product", lazy="select")


class ProductScore(Base):
    __tablename__ = "product_scores"

    id = Column(Integer, primary_key=True, index=True)
    ad_id = Column(Integer, ForeignKey("scraped_ads.id"), nullable=False)
    score = Column(Float, nullable=False, index=True)
    engagement_score = Column(Float)
    problem_solution_bonus = Column(Float)
    category_bonus = Column(Float)
    multi_posting_bonus = Column(Float)
    recency_score = Column(Float)
    calculated_at = Column(DateTime, server_default=func.now())

    # Relationships
    ad = relationship("ScrapedAd", back_populates="product_score")

