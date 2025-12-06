import httpx
from typing import List, Dict, Any, Optional
import asyncio
import logging
from app.config import settings
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


class CreatifyService:
    BASE_URL = "https://api.creatify.ai/api"

    def __init__(self):
        if not settings.creatify_api_id or not settings.creatify_api_key:
            raise ValueError("CREATIFY_API_ID and CREATIFY_API_KEY not configured")
        self.api_id = settings.creatify_api_id
        self.api_key = settings.creatify_api_key
        self.headers = {
            "X-API-ID": self.api_id,
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    @retry_on_failure(max_retries=3, delay=1.0)
    async def generate_video_from_url(
        self,
        product_url: str,
        video_type: str = "ugc",
        voice_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Génère une vidéo à partir d'une URL produit

        Paramètres:
        - product_url: URL de la page produit
        - video_type: "ugc", "problem_solution", "short_hook", "carousel"
        - voice_id: ID de la voix (optionnel)
        """
        video_configs = {
            "ugc": {
                "aspect_ratio": "9:16",
                "duration": "20-30",
                "style": "ugc",
                "include_captions": True
            },
            "problem_solution": {
                "aspect_ratio": "1:1",
                "duration": "30-45",
                "style": "professional",
                "structure": "problem_solution"
            },
            "short_hook": {
                "aspect_ratio": "9:16",
                "duration": "6-10",
                "style": "fast_paced",
                "hook_focused": True
            },
            "carousel": {
                "aspect_ratio": "1:1",
                "duration": "30-60",
                "style": "showcase",
                "multi_angle": True
            }
        }

        config = video_configs.get(video_type, video_configs["ugc"])

        payload = {
            "url": product_url,
            "aspect_ratio": config["aspect_ratio"],
            "duration_range": config["duration"],
            "video_style": config["style"],
            "voice_id": voice_id,
            "include_captions": config.get("include_captions", False),
            "ai_avatar": True,
            "music_enabled": True
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.BASE_URL}/video/generate",
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                logger.info(f"Vidéo {video_type} générée - ID: {data.get('video_id')}")
                return data

        except httpx.HTTPError as e:
            logger.error(f"Erreur Creatify API: {str(e)}")
            raise

    @retry_on_failure(max_retries=3, delay=1.0)
    async def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """
        Vérifie le statut de génération d'une vidéo

        Statuts possibles: "queued", "processing", "completed", "failed"
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/video/{video_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"Erreur récupération statut vidéo: {str(e)}")
            raise

    async def download_video(self, video_id: str, save_path: str) -> str:
        """
        Télécharge une vidéo terminée

        Retourne: chemin du fichier sauvegardé
        """
        # D'abord récupérer le statut pour obtenir l'URL de téléchargement
        status_data = await self.get_video_status(video_id)

        if status_data.get("status") != "completed":
            raise ValueError(f"Vidéo pas encore prête: {status_data.get('status')}")

        download_url = status_data.get("download_url")
        if not download_url:
            raise ValueError("URL de téléchargement introuvable")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(download_url)
                response.raise_for_status()

                # Sauvegarder le fichier
                import os
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(response.content)

                logger.info(f"Vidéo téléchargée: {save_path}")
                return save_path

        except httpx.HTTPError as e:
            logger.error(f"Erreur téléchargement vidéo: {str(e)}")
            raise

    async def generate_all_creatives_for_product(
        self,
        product_url: str,
        product_id: int
    ) -> List[Dict[str, Any]]:
        """
        Génère les 4 types de créatives pour un produit

        Retourne: Liste des infos des vidéos générées
        """
        video_types = ["ugc", "problem_solution", "short_hook", "carousel"]

        tasks = []
        for vtype in video_types:
            task = self.generate_video_from_url(product_url, vtype)
            tasks.append(task)

        # Lancer en parallèle
        results = await asyncio.gather(*tasks, return_exceptions=True)

        creatives = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Erreur génération {video_types[i]}: {str(result)}")
                continue

            creatives.append({
                "product_id": product_id,
                "video_id": result.get("video_id"),
                "video_type": video_types[i],
                "status": result.get("status", "queued"),
                "estimated_completion": result.get("estimated_time")
            })

        return creatives

