from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.ads import ScrapedAd
from app.models.orders import Order
from app.schemas.orders import OrderCreateRequest, OrderResponse
from sqlalchemy import select
import logging

router = APIRouter(prefix="/api/orders", tags=["orders"])
logger = logging.getLogger(__name__)


@router.post("", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Crée une nouvelle commande
    """
    # Vérifier que le produit existe
    result = await db.execute(
        select(ScrapedAd).where(ScrapedAd.id == order_data.productId)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # Créer la commande
    order = Order(
        product_id=order_data.productId,
        product_name=order_data.productName or f"Produit {order_data.productId}",
        full_name=order_data.fullName,
        phone=order_data.phone,
        address=order_data.address,
        city=order_data.city,
        quantity=order_data.quantity,
        status="pending"
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    logger.info(f"Commande créée - ID: {order.id}, Produit: {order.product_id}")

    return OrderResponse(
        id=order.id,
        orderId=order.id,
        message="Commande enregistrée avec succès"
    )

