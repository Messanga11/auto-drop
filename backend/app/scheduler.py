from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.scraping_service import ScrapingService
from app.database import get_db
from app.models.ads import ScrapedAd
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


async def monthly_scraping_job():
    """
    Tâche planifiée: scraping mensuel automatique
    S'exécute le 1er de chaque mois à 2h du matin
    """
    logger.info("Démarrage du scraping mensuel automatique")

    try:
        scraper = ScrapingService()
        async for db in get_db():
            # Scraper Facebook (500 ads)
            fb_ads = await scraper.scrape_facebook_ads(max_items=500)
            for raw_ad in fb_ads:
                normalized = scraper.normalize_facebook_ad(raw_ad)
                # Vérifier si l'ad existe déjà
                from sqlalchemy import select
                existing = await db.execute(
                    select(ScrapedAd).where(ScrapedAd.ad_id == normalized["ad_id"])
                )
                if existing.scalar_one_or_none():
                    continue
                ad = ScrapedAd(**normalized)
                db.add(ad)

            # Scraper TikTok (500 ads)
            tt_ads = await scraper.scrape_tiktok_ads(max_pages=50)
            for raw_ad in tt_ads:
                normalized = scraper.normalize_tiktok_ad(raw_ad)
                # Vérifier si l'ad existe déjà
                from sqlalchemy import select
                existing = await db.execute(
                    select(ScrapedAd).where(ScrapedAd.ad_id == normalized["ad_id"])
                )
                if existing.scalar_one_or_none():
                    continue
                ad = ScrapedAd(**normalized)
                db.add(ad)

            await db.commit()

        logger.info("Scraping mensuel terminé avec succès")

    except Exception as e:
        logger.error(f"Erreur scraping mensuel: {str(e)}")


def start_scheduler():
    """Démarre le scheduler avec toutes les tâches planifiées"""

    # Scraping mensuel: 1er du mois à 02:00
    scheduler.add_job(
        monthly_scraping_job,
        trigger=CronTrigger(day=1, hour=2, minute=0),
        id="monthly_scraping",
        name="Scraping mensuel automatique",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Scheduler démarré - Tâches planifiées actives")

