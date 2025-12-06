import httpx
from typing import Dict, Any, List
import logging
from app.config import settings
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)

# TikTok Ads API v1.3
TIKTOK_API_BASE = "https://business-api.tiktok.com/open_api/v1.3"


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
                        wait_time = delay * (2 ** attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}, "
                            f"retrying in {wait_time}s..."
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}"
                        )
            raise last_exception
        return wrapper
    return decorator


class TikTokAdsService:
    def __init__(self):
        if not settings.tiktok_access_token or not settings.tiktok_advertiser_id:
            raise ValueError("TikTok Ads credentials not configured")

        self.access_token = settings.tiktok_access_token
        self.advertiser_id = settings.tiktok_advertiser_id
        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_campaign(
        self,
        campaign_name: str,
        daily_budget: int = 5000,  # En centimes
        objective: str = "TRAFFIC"
    ) -> Dict[str, Any]:
        """Crée une campagne TikTok Ads"""

        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_name": campaign_name,
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": daily_budget,
            "operation_status": "ENABLE",
            "objective_type": objective
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TIKTOK_API_BASE}/campaign/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise ValueError(f"TikTok API error: {data.get('message')}")

                campaign_id = data["data"]["campaign_id"]
                logger.info(f"Campagne TikTok créée - ID: {campaign_id}")

                return {
                    "campaign_id": str(campaign_id),
                    "name": campaign_name,
                    "status": "created"
                }

        except httpx.HTTPError as e:
            logger.error(f"Erreur création campagne TikTok: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_ad_group(
        self,
        campaign_id: str,
        adgroup_name: str,
        daily_budget: int = 2000,
        optimization_goal: str = "CLICK"
    ) -> Dict[str, Any]:
        """Crée un ad group dans une campagne"""

        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_id": campaign_id,
            "adgroup_name": adgroup_name,
            "budget_mode": "BUDGET_MODE_DAY",
            "budget": daily_budget,
            "optimization_goal": optimization_goal,
            "operation_status": "ENABLE",
            "placement_type": "AUTOMATIC",
            "targeting": {
                "age_range": [18, 65],
                "genders": [1, 2],  # Male, Female
                "geo_locations": {
                    "included": [
                        {"region_code": "FR"},
                        {"region_code": "CM"}
                    ]
                }
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TIKTOK_API_BASE}/adgroup/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise ValueError(f"TikTok API error: {data.get('message')}")

                adgroup_id = data["data"]["adgroup_id"]
                logger.info(f"AdGroup TikTok créé - ID: {adgroup_id}")

                return {
                    "adgroup_id": str(adgroup_id),
                    "name": adgroup_name,
                    "status": "created"
                }

        except httpx.HTTPError as e:
            logger.error(f"Erreur création adgroup TikTok: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def upload_video(self, video_path: str) -> str:
        """Upload une vidéo et retourne son ID"""

        try:
            # TikTok nécessite un upload en 2 étapes
            # 1. Initier l'upload
            async with httpx.AsyncClient() as client:
                init_response = await client.post(
                    f"{TIKTOK_API_BASE}/file/video/ad/upload/",
                    headers=self.headers,
                    json={
                        "advertiser_id": self.advertiser_id
                    }
                )
                init_response.raise_for_status()
                init_data = init_response.json()

                upload_url = init_data["data"]["upload_url"]
                video_id = init_data["data"]["video_id"]

                # 2. Upload le fichier
                with open(video_path, "rb") as f:
                    upload_response = await client.put(
                        upload_url,
                        content=f.read()
                    )
                    upload_response.raise_for_status()

                logger.info(f"Vidéo TikTok uploadée - ID: {video_id}")
                return video_id

        except Exception as e:
            logger.error(f"Erreur upload vidéo TikTok: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_ad(
        self,
        adgroup_id: str,
        ad_name: str,
        video_id: str,
        landing_page_url: str,
        ad_text: str
    ) -> Dict[str, Any]:
        """Crée une publicité vidéo"""

        payload = {
            "advertiser_id": self.advertiser_id,
            "adgroup_id": adgroup_id,
            "ad_name": ad_name,
            "ad_text": ad_text,
            "video_id": video_id,
            "landing_page_url": landing_page_url,
            "call_to_action": "LEARN_MORE",
            "operation_status": "ENABLE"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TIKTOK_API_BASE}/ad/create/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise ValueError(f"TikTok API error: {data.get('message')}")

                ad_id = data["data"]["ad_id"]
                logger.info(f"Ad TikTok créée - ID: {ad_id}")

                return {
                    "ad_id": str(ad_id),
                    "name": ad_name,
                    "status": "created"
                }

        except httpx.HTTPError as e:
            logger.error(f"Erreur création ad TikTok: {str(e)}")
            raise

    async def activate_campaign(self, campaign_id: str) -> bool:
        """Active une campagne TikTok"""

        payload = {
            "advertiser_id": self.advertiser_id,
            "campaign_ids": [campaign_id],
            "operation_status": "ENABLE"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{TIKTOK_API_BASE}/campaign/update/status/",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                if data.get("code") != 0:
                    raise ValueError(f"TikTok API error: {data.get('message')}")

                logger.info(f"Campagne TikTok {campaign_id} activée")
                return True

        except Exception as e:
            logger.error(f"Erreur activation campagne TikTok: {str(e)}")
            return False

