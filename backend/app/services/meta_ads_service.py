from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.advideo import AdVideo
from typing import Dict, Any, List
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


class MetaAdsService:
    def __init__(self):
        if not all([
            settings.meta_app_id,
            settings.meta_app_secret,
            settings.meta_access_token,
            settings.meta_ad_account_id
        ]):
            raise ValueError("Meta Ads credentials not configured")

        # Initialiser l'API Facebook
        FacebookAdsApi.init(
            settings.meta_app_id,
            settings.meta_app_secret,
            settings.meta_access_token
        )

        self.ad_account = AdAccount(f"act_{settings.meta_ad_account_id}")

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_campaign(
        self,
        campaign_name: str,
        daily_budget: int = 5000,  # En centimes (50€)
        objective: str = "OUTCOME_TRAFFIC"
    ) -> Dict[str, Any]:
        """Crée une campagne Meta Ads"""

        params = {
            Campaign.Field.name: campaign_name,
            Campaign.Field.objective: objective,
            Campaign.Field.status: Campaign.Status.paused,
            Campaign.Field.special_ad_categories: [],
            Campaign.Field.daily_budget: daily_budget
        }

        try:
            loop = asyncio.get_event_loop()
            campaign = await loop.run_in_executor(
                None,
                lambda: self.ad_account.create_campaign(params=params)
            )

            logger.info(f"Campagne créée - ID: {campaign['id']}")
            return {
                "campaign_id": campaign['id'],
                "name": campaign_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création campagne: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_adset(
        self,
        campaign_id: str,
        adset_name: str,
        daily_budget: int = 2000,
        targeting: Dict[str, Any] = None,
        optimization_goal: str = "LINK_CLICKS"
    ) -> Dict[str, Any]:
        """Crée un ad set dans une campagne"""

        if not targeting:
            targeting = {
                'geo_locations': {
                    'countries': ['FR', 'CM']
                },
                'age_min': 18,
                'age_max': 65,
            }

        params = {
            AdSet.Field.name: adset_name,
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.daily_budget: daily_budget,
            AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
            AdSet.Field.optimization_goal: optimization_goal,
            AdSet.Field.bid_strategy: AdSet.BidStrategy.lowest_cost_without_cap,
            AdSet.Field.targeting: targeting,
            AdSet.Field.status: AdSet.Status.paused,
            AdSet.Field.promoted_object: {
                'pixel_id': settings.meta_pixel_id
            }
        }

        try:
            loop = asyncio.get_event_loop()
            adset = await loop.run_in_executor(
                None,
                lambda: AdSet(parent_id=settings.meta_ad_account_id).api_create(params=params)
            )

            logger.info(f"AdSet créé - ID: {adset['id']}")
            return {
                "adset_id": adset['id'],
                "name": adset_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création adset: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def upload_video_creative(
        self,
        video_path: str,
        video_title: str
    ) -> str:
        """Upload une vidéo et retourne son ID"""

        try:
            loop = asyncio.get_event_loop()
            video = AdVideo(parent_id=settings.meta_ad_account_id)
            video[AdVideo.Field.filepath] = video_path
            video[AdVideo.Field.name] = video_title

            await loop.run_in_executor(
                None,
                lambda: video.api_create()
            )
            await loop.run_in_executor(
                None,
                lambda: video.waitUntilEncodingReady()
            )

            logger.info(f"Vidéo uploadée - ID: {video['id']}")
            return video['id']

        except Exception as e:
            logger.error(f"Erreur upload vidéo: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def create_video_ad(
        self,
        adset_id: str,
        ad_name: str,
        video_id: str,
        page_id: str,
        message: str,
        link: str,
        call_to_action: str = "LEARN_MORE"
    ) -> Dict[str, Any]:
        """Crée une publicité vidéo"""

        creative = AdCreative(parent_id=settings.meta_ad_account_id)
        creative[AdCreative.Field.name] = f"{ad_name} - Creative"
        creative[AdCreative.Field.object_story_spec] = {
            'page_id': page_id,
            'video_data': {
                'video_id': video_id,
                'message': message,
                'call_to_action': {
                    'type': call_to_action,
                    'value': {
                        'link': link
                    }
                }
            }
        }

        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: creative.api_create()
            )

            ad = Ad(parent_id=settings.meta_ad_account_id)
            ad[Ad.Field.name] = ad_name
            ad[Ad.Field.adset_id] = adset_id
            ad[Ad.Field.creative] = {'creative_id': creative['id']}
            ad[Ad.Field.status] = Ad.Status.paused

            await loop.run_in_executor(
                None,
                lambda: ad.api_create()
            )

            logger.info(f"Ad créée - ID: {ad['id']}")
            return {
                "ad_id": ad['id'],
                "creative_id": creative['id'],
                "name": ad_name,
                "status": "created"
            }

        except Exception as e:
            logger.error(f"Erreur création ad: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def activate_campaign(self, campaign_id: str) -> bool:
        """Active une campagne"""

        try:
            loop = asyncio.get_event_loop()
            campaign = Campaign(campaign_id)
            await loop.run_in_executor(
                None,
                lambda: campaign.api_update(params={
                    Campaign.Field.status: Campaign.Status.active
                })
            )

            logger.info(f"Campagne {campaign_id} activée")
            return True

        except Exception as e:
            logger.error(f"Erreur activation campagne: {str(e)}")
            return False

    async def create_complete_campaign_for_product(
        self,
        product_id: int,
        product_name: str,
        landing_page_url: str,
        video_paths: List[str],
        daily_budget: int = 5000
    ) -> Dict[str, Any]:
        """Workflow complet: crée campagne + adsets + ads pour un produit"""

        campaign_data = await self.create_campaign(
            campaign_name=f"Campagne - {product_name}",
            daily_budget=daily_budget,
            objective="OUTCOME_TRAFFIC"
        )

        campaign_id = campaign_data["campaign_id"]
        budget_per_adset = daily_budget // len(video_paths) if video_paths else daily_budget
        ads_created = []

        for idx, video_path in enumerate(video_paths):
            video_type = video_path.split("_")[-1].split(".")[0]

            adset_data = await self.create_adset(
                campaign_id=campaign_id,
                adset_name=f"{product_name} - {video_type}",
                daily_budget=budget_per_adset,
                optimization_goal="LINK_CLICKS"
            )

            video_id = await self.upload_video_creative(
                video_path=video_path,
                video_title=f"{product_name} - {video_type}"
            )

            ad_data = await self.create_video_ad(
                adset_id=adset_data["adset_id"],
                ad_name=f"{product_name} - Ad {idx+1}",
                video_id=video_id,
                page_id=settings.meta_page_id,
                message=f"Découvrez {product_name} - Commandez maintenant!",
                link=landing_page_url,
                call_to_action="LEARN_MORE"
            )

            ads_created.append(ad_data)

        logger.info(f"Campagne complète créée pour {product_name}")
        return {
            "campaign_id": campaign_id,
            "adsets_count": len(video_paths),
            "ads": ads_created,
            "status": "ready_to_activate"
        }

