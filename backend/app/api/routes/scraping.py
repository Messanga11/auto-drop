from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.scraping_service import ScrapingService
from app.database import get_db
from app.models.ads import ScrapedAd
from app.schemas.scraping import ScrapingStartRequest, ScrapingStartResponse, ScrapingStatusResponse
from typing import Dict, Any
import logging

router = APIRouter(prefix="/scraping", tags=["scraping"])
logger = logging.getLogger(__name__)


@router.post("/start", response_model=ScrapingStartResponse)
async def start_scraping(
    request: ScrapingStartRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance le scraping des publicités Facebook et TikTok en arrière-plan

    Paramètres:
    - facebook_max: nombre maximum d'ads Facebook à scraper
    - tiktok_max: nombre maximum de pages TikTok à scraper
    """

    async def run_scraping_task():
        try:
            scraper = ScrapingService()

            # Scraper Facebook
            logger.info("Démarrage scraping Facebook...")
            fb_ads = await scraper.scrape_facebook_ads(max_items=request.facebook_max)

            # Sauvegarder en BDD
            for raw_ad in fb_ads:
                normalized_ad = scraper.normalize_facebook_ad(raw_ad)
                # Vérifier si l'ad existe déjà
                from sqlalchemy import select
                existing = await db.execute(
                    select(ScrapedAd).where(ScrapedAd.ad_id == normalized_ad["ad_id"])
                )
                if existing.scalar_one_or_none():
                    continue
                ad = ScrapedAd(**normalized_ad)
                db.add(ad)

            await db.commit()
            logger.info(f"{len(fb_ads)} ads Facebook sauvegardées")

            # Scraper TikTok
            logger.info("Démarrage scraping TikTok...")
            tt_ads = await scraper.scrape_tiktok_ads(max_pages=request.tiktok_max)

            # Sauvegarder en BDD
            for raw_ad in tt_ads:
                normalized_ad = scraper.normalize_tiktok_ad(raw_ad)
                # Vérifier si l'ad existe déjà
                from sqlalchemy import select
                existing = await db.execute(
                    select(ScrapedAd).where(ScrapedAd.ad_id == normalized_ad["ad_id"])
                )
                if existing.scalar_one_or_none():
                    continue
                ad = ScrapedAd(**normalized_ad)
                db.add(ad)

            await db.commit()
            logger.info(f"{len(tt_ads)} ads TikTok sauvegardées")

            logger.info("Scraping terminé avec succès")

        except Exception as e:
            logger.error(f"Erreur lors du scraping: {str(e)}")
            raise

    # Lancer la tâche en arrière-plan
    background_tasks.add_task(run_scraping_task)

    return ScrapingStartResponse(
        status="started",
        message="Le scraping a été lancé en arrière-plan",
        facebook_max=request.facebook_max,
        tiktok_max=request.tiktok_max
    )


@router.get("/status", response_model=ScrapingStatusResponse)
async def get_scraping_status(db: AsyncSession = Depends(get_db)):
    """Récupère le statut actuel du scraping"""
    from sqlalchemy import select, func
    from app.models.ads import ScrapedAd

    # Compter les ads par plateforme
    result = await db.execute(
        select(
            ScrapedAd.platform,
            func.count(ScrapedAd.id).label("count")
        ).group_by(ScrapedAd.platform)
    )

    counts = {row.platform: row.count for row in result}

    return ScrapingStatusResponse(
        total_ads=sum(counts.values()),
        facebook_ads=counts.get("facebook", 0),
        tiktok_ads=counts.get("tiktok", 0)
    )

