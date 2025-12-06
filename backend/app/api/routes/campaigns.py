from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.meta_ads_service import MetaAdsService
from app.services.tiktok_ads_service import TikTokAdsService
from app.database import get_db
from app.models.ads import ScrapedAd
from app.models.campaigns import Campaign, Creative
from sqlalchemy import select
from typing import List, Dict, Any
import logging
import os

router = APIRouter(prefix="/campaigns", tags=["campaigns"])
logger = logging.getLogger(__name__)


@router.post("/launch-for-product/{product_id}", response_model=Dict[str, Any])
async def launch_campaign_for_product(
    product_id: int,
    platform: str = "meta",  # "meta" ou "tiktok"
    daily_budget: int = 5000,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance une campagne publicitaire pour un produit sur Meta ou TikTok
    """
    # Récupérer le produit
    result = await db.execute(
        select(ScrapedAd).where(ScrapedAd.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # Récupérer les créatives du produit
    creatives_result = await db.execute(
        select(Creative).where(
            Creative.product_id == product_id,
            Creative.status == "completed"
        )
    )
    creatives = creatives_result.scalars().all()

    if not creatives:
        raise HTTPException(
            status_code=400,
            detail="Aucune créative complétée pour ce produit"
        )

    # Construire l'URL de la landing page
    from app.config import settings
    landing_page_url = f"{settings.frontend_url}/p/{product_id}"

    async def launch_task():
        try:
            video_paths = []
            for creative in creatives:
                if creative.local_path:
                    video_paths.append(creative.local_path)

            if platform == "meta":
                service = MetaAdsService()
                campaign_data = await service.create_complete_campaign_for_product(
                    product_id=product_id,
                    product_name=product.page_name or f"Produit {product_id}",
                    landing_page_url=landing_page_url,
                    video_paths=video_paths,
                    daily_budget=daily_budget
                )
            elif platform == "tiktok":
                # Pour TikTok, créer campagne + adgroups + ads
                service = TikTokAdsService()
                campaign_data = await service.create_campaign(
                    campaign_name=f"Campagne - Produit {product_id}",
                    daily_budget=daily_budget
                )
                # TODO: Créer adgroups et ads pour chaque créative
                campaign_data = {
                    "campaign_id": campaign_data["campaign_id"],
                    "status": "created"
                }
            else:
                raise ValueError(f"Plateforme inconnue: {platform}")

            # Sauvegarder en BDD
            campaign = Campaign(
                product_id=product_id,
                platform=platform,
                campaign_id=campaign_data["campaign_id"],
                campaign_name=f"Campagne - Produit {product_id}",
                daily_budget=daily_budget,
                status="created",
                meta_data=campaign_data
            )
            db.add(campaign)
            await db.commit()

            logger.info(f"Campagne {platform} créée pour produit {product_id}")

        except Exception as e:
            logger.error(f"Erreur lancement campagne: {str(e)}")

    if background_tasks:
        background_tasks.add_task(launch_task)
    else:
        await launch_task()

    return {
        "status": "started",
        "message": f"Campagne {platform} lancée pour le produit {product_id}",
        "platform": platform
    }


@router.post("/activate/{campaign_id}", response_model=Dict[str, Any])
async def activate_campaign(
    campaign_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Active une campagne (passe de PAUSED à ACTIVE)"""
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id)
    )
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne introuvable")

    try:
        if campaign.platform == "meta":
            service = MetaAdsService()
            success = await service.activate_campaign(campaign.campaign_id)
        elif campaign.platform == "tiktok":
            service = TikTokAdsService()
            success = await service.activate_campaign(campaign.campaign_id)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Plateforme inconnue: {campaign.platform}"
            )

        if success:
            campaign.status = "active"
            await db.commit()

            return {
                "status": "activated",
                "message": f"Campagne {campaign_id} activée avec succès"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de l'activation de la campagne"
            )

    except Exception as e:
        logger.error(f"Erreur activation campagne: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

