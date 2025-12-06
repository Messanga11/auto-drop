from fastapi import APIRouter, Request, Query, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.whatsapp_service import WhatsAppService
from app.database import get_db
from app.config import settings
from typing import Dict, Any
import logging
import hmac
import hashlib

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str = Query(..., alias="hub.mode"),
    hub_verify_token: str = Query(..., alias="hub.verify_token"),
    hub_challenge: str = Query(..., alias="hub.challenge")
):
    """
    Endpoint de vérification pour le webhook WhatsApp
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("Webhook WhatsApp vérifié avec succès")
        return PlainTextResponse(hub_challenge)
    else:
        logger.warning("Échec vérification webhook WhatsApp")
        raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/whatsapp")
async def handle_whatsapp_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Endpoint pour recevoir les messages WhatsApp entrants
    """
    try:
        body = await request.json()
        logger.info(f"Webhook WhatsApp reçu: {body}")

        # Vérifier la signature (optionnel mais recommandé)
        # signature = request.headers.get("X-Hub-Signature-256")
        # if signature:
        #     # Vérifier la signature avec le secret
        #     pass

        # Extraire les données du webhook
        entry = body.get("entry", [])
        if not entry:
            return {"status": "ok"}

        changes = entry[0].get("changes", [])
        if not changes:
            return {"status": "ok"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ok"}

        # Traiter chaque message
        whatsapp_service = WhatsAppService()

        for message in messages:
            from_number = message.get("from")
            message_text = message.get("text", {}).get("body", "")
            message_id = message.get("id")

            if not message_text:
                continue

            # Traiter le message et envoyer une réponse
            await whatsapp_service.handle_incoming_message(
                from_number=from_number,
                message_text=message_text,
                message_id=message_id,
                db_session=db
            )

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Erreur traitement webhook WhatsApp: {str(e)}")
        return {"status": "error", "error": str(e)}

