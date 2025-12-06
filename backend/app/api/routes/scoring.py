from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scoring_service import ScoringService
from app.database import get_db
from app.schemas.scoring import ScoringCalculateResponse, TopProductResponse
from typing import List, Dict, Any
from sqlalchemy import select, desc
from app.models.ads import ProductScore, ScrapedAd

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.post("/calculate", response_model=ScoringCalculateResponse)
async def calculate_scores(db: AsyncSession = Depends(get_db)):
    """
    Lance le calcul des scores pour toutes les ads non scorées
    Retourne les 5 meilleurs produits identifiés
    """
    scoring_service = ScoringService(db)

    try:
        top_5 = await scoring_service.calculate_scores_for_all_ads()

        if not top_5:
            raise HTTPException(
                status_code=404,
                detail="Aucun produit trouvé après scoring"
            )

        top_5_products = [
            TopProductResponse(
                product_id=item["ad_id"],
                platform=item["platform"],
                score=item["score"],
                ad_url=item.get("ad_url")
            )
            for item in top_5
        ]

        return ScoringCalculateResponse(
            status="success",
            top_5_products=top_5_products,
            message=f"{len(top_5)} produits sélectionnés"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-products", response_model=List[TopProductResponse])
async def get_top_products(
    limit: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """Récupère les N meilleurs produits déjà scorés"""
    result = await db.execute(
        select(ProductScore, ScrapedAd)
        .join(ScrapedAd, ProductScore.ad_id == ScrapedAd.id)
        .order_by(desc(ProductScore.score))
        .limit(limit)
    )

    products = []
    for score, ad in result:
        products.append(
            TopProductResponse(
                product_id=ad.id,
                platform=ad.platform,
                score=score.score,
                ad_url=ad.ad_snapshot_url or ad.video_url,
                page_name=ad.page_name or ad.advertiser_name,
                caption=ad.ad_creative_bodies or ad.caption
            )
        )

    return products

