from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.creatify_service import CreatifyService
from app.database import get_db
from app.models.ads import ScrapedAd
from app.models.campaigns import Creative
from typing import List, Dict, Any
from sqlalchemy import select
import logging

router = APIRouter(prefix="/creatives", tags=["creatives"])
logger = logging.getLogger(__name__)


@router.post("/generate/{product_id}", response_model=Dict[str, Any])
async def generate_creatives_for_product(
    product_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Lance la génération des 4 créatives pour un produit
    """
    # Récupérer le produit
    result = await db.execute(
        select(ScrapedAd).where(ScrapedAd.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    product_url = product.ad_snapshot_url or product.video_url
    if not product_url:
        raise HTTPException(
            status_code=400,
            detail="Aucune URL produit disponible"
        )

    async def generate_task():
        try:
            creatify = CreatifyService()
            creatives_data = await creatify.generate_all_creatives_for_product(
                product_url,
                product_id
            )

            # Sauvegarder en BDD
            for creative_data in creatives_data:
                creative = Creative(
                    product_id=product_id,
                    video_id=creative_data["video_id"],
                    video_type=creative_data["video_type"],
                    status=creative_data["status"]
                )
                db.add(creative)

            await db.commit()
            logger.info(f"{len(creatives_data)} créatives générées pour produit {product_id}")

        except Exception as e:
            logger.error(f"Erreur génération créatives: {str(e)}")

    background_tasks.add_task(generate_task)

    return {
        "status": "started",
        "message": f"Génération de 4 créatives lancée pour le produit {product_id}",
        "product_url": product_url
    }


@router.get("/status/{product_id}", response_model=List[Dict[str, Any]])
async def get_creatives_status(
    product_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Récupère le statut de toutes les créatives d'un produit"""
    result = await db.execute(
        select(Creative).where(Creative.product_id == product_id)
    )
    creatives = result.scalars().all()

    if not creatives:
        raise HTTPException(
            status_code=404,
            detail="Aucune créative trouvée pour ce produit"
        )

    creatify = CreatifyService()
    status_list = []

    for creative in creatives:
        try:
            status_data = await creatify.get_video_status(creative.video_id)
            status_list.append({
                "creative_id": creative.id,
                "video_type": creative.video_type,
                "status": status_data.get("status"),
                "progress": status_data.get("progress", 0),
                "download_url": status_data.get("download_url")
            })
        except Exception as e:
            logger.error(f"Erreur statut créative {creative.id}: {str(e)}")

    return status_list

