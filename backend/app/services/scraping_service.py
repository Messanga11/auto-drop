from apify_client import ApifyClient
from typing import List, Dict, Any
from datetime import datetime, timedelta
import logging
from app.config import settings
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying failed API calls"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator


class ScrapingService:
    def __init__(self):
        if not settings.apify_api_token:
            raise ValueError("APIFY_API_TOKEN not configured")
        self.client = ApifyClient(settings.apify_api_token)

    @retry_on_failure(max_retries=3, delay=1.0)
    async def scrape_facebook_ads(
        self,
        max_items: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Scrape Facebook Ads Library

        Paramètres:
        - max_items: nombre maximum d'ads à récupérer

        Retourne: Liste de dictionnaires contenant les données des ads
        """
        actor_id = "curious_coder/facebook-ads-library-scraper"

        run_input = {
            "searchTerms": [
                "dropshipping",
                "trending product",
                "buy now",
                "limited offer"
            ],
            "countries": ["FR", "US", "GB", "CA", "DE"],
            "maxItems": max_items,
            "minLikes": 500,
            "minComments": 20,
            "datePreset": "last_30d",
            "proxyConfiguration": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"]
            }
        }

        try:
            logger.info(f"Démarrage scraping Facebook Ads - Actor: {actor_id}")
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            run = await loop.run_in_executor(
                None,
                lambda: self.client.actor(actor_id).call(run_input=run_input)
            )

            # Récupérer les résultats du dataset
            dataset_items = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)

            logger.info(f"Scraping Facebook terminé - {len(dataset_items)} ads récupérées")
            return dataset_items

        except Exception as e:
            logger.error(f"Erreur scraping Facebook: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def scrape_tiktok_ads(
        self,
        max_pages: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Scrape TikTok Ads Library

        Paramètres:
        - max_pages: nombre maximum de pages à scraper

        Retourne: Liste de dictionnaires contenant les données des ads
        """
        actor_id = "lexis-solutions/tiktok-ads-scraper"

        # Dates pour les 30 derniers jours
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        run_input = {
            "queries": [
                "dropshipping",
                "trending products",
                "viral products",
                "must have"
            ],
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "maxPages": max_pages,
            "regions": ["FR", "US", "GB", "CA", "DE"]
        }

        try:
            logger.info(f"Démarrage scraping TikTok Ads - Actor: {actor_id}")
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            run = await loop.run_in_executor(
                None,
                lambda: self.client.actor(actor_id).call(run_input=run_input)
            )

            # Récupérer les résultats
            dataset_items = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                dataset_items.append(item)

            logger.info(f"Scraping TikTok terminé - {len(dataset_items)} ads récupérées")
            return dataset_items

        except Exception as e:
            logger.error(f"Erreur scraping TikTok: {str(e)}")
            raise

    def normalize_facebook_ad(self, raw_ad: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliser les données Facebook pour la BDD"""
        ad_creative_bodies = raw_ad.get("ad_creative_bodies", [])
        if isinstance(ad_creative_bodies, list):
            ad_creative_bodies = " ".join(ad_creative_bodies)
        
        ad_delivery_start_time = raw_ad.get("ad_delivery_start_time")
        if isinstance(ad_delivery_start_time, str):
            try:
                ad_delivery_start_time = datetime.fromisoformat(
                    ad_delivery_start_time.replace('Z', '+00:00')
                )
            except (ValueError, AttributeError):
                ad_delivery_start_time = None

        return {
            "platform": "facebook",
            "ad_id": str(raw_ad.get("ad_id", "")),
            "ad_snapshot_url": raw_ad.get("ad_snapshot_url"),
            "page_name": raw_ad.get("page_name"),
            "ad_creative_bodies": ad_creative_bodies,
            "ad_delivery_start_time": ad_delivery_start_time,
            "impressions_upper_bound": (
                raw_ad.get("impressions", {}).get("upper_bound")
                if isinstance(raw_ad.get("impressions"), dict)
                else None
            ),
            "likes": raw_ad.get("likes", 0) or 0,
            "comments": raw_ad.get("comments", 0) or 0,
            "shares": raw_ad.get("shares", 0) or 0,
            "views": raw_ad.get("views", 0) or 0,
        }

    def normalize_tiktok_ad(self, raw_ad: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliser les données TikTok pour la BDD"""
        first_shown_date = raw_ad.get("first_shown_date")
        if isinstance(first_shown_date, str):
            try:
                first_shown_date = datetime.fromisoformat(
                    first_shown_date.replace('Z', '+00:00')
                )
            except (ValueError, AttributeError):
                first_shown_date = None

        return {
            "platform": "tiktok",
            "ad_id": str(raw_ad.get("ad_id", "")),
            "advertiser_name": raw_ad.get("advertiser_name"),
            "caption": raw_ad.get("caption"),
            "video_url": raw_ad.get("video_url"),
            "likes": raw_ad.get("likes", 0) or 0,
            "comments": raw_ad.get("comments", 0) or 0,
            "shares": raw_ad.get("shares", 0) or 0,
            "views": raw_ad.get("views", 0) or 0,
            "first_shown_date": first_shown_date,
        }

