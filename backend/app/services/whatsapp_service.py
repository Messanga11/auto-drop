import httpx
import ollama
from typing import Dict, Any, Optional
import logging
from app.config import settings
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

# WhatsApp Cloud API
WHATSAPP_API_BASE = "https://graph.facebook.com/v21.0"


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


class WhatsAppService:
    def __init__(self):
        if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
            raise ValueError("WhatsApp credentials not configured")

        self.access_token = settings.whatsapp_access_token
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.ollama_client = ollama.AsyncClient(host=settings.ollama_host)

    @retry_on_failure(max_retries=3, delay=1.0)
    async def send_message(
        self,
        to: str,
        message: str,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Envoie un message WhatsApp

        Paramètres:
        - to: Numéro de téléphone du destinataire (format: 237XXXXXXXXX)
        - message: Contenu du message
        - message_type: "text" ou "template"
        """
        url = f"{WHATSAPP_API_BASE}/{self.phone_number_id}/messages"

        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": message_type,
            "text": {
                "body": message
            }
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()

                logger.info(f"Message WhatsApp envoyé à {to}")
                return data

        except httpx.HTTPError as e:
            logger.error(f"Erreur envoi message WhatsApp: {str(e)}")
            raise

    async def generate_ai_response(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Génère une réponse IA en utilisant Ollama

        Paramètres:
        - user_message: Message de l'utilisateur
        - context: Contexte additionnel (ex: commande en cours)
        """
        system_prompt = """Tu es un assistant commercial pour une plateforme de dropshipping.
Tu dois être professionnel, amical et aider les clients avec leurs commandes.
Réponds en français de manière concise et utile."""

        if context:
            context_str = f"\nContexte: Commande #{context.get('order_id')} - {context.get('product_name')} (Statut: {context.get('status')})"
        else:
            context_str = ""

        full_prompt = f"{system_prompt}{context_str}\n\nMessage client: {user_message}\n\nRéponse:"

        # Fallback messages selon le contexte
        fallback_messages = {
            "order": "Merci pour votre message ! Votre commande est en cours de traitement. Nous vous tiendrons informé de son avancement.",
            "general": "Bonjour ! Merci de nous avoir contactés. Comment puis-je vous aider aujourd'hui ?",
            "error": "Désolé, je rencontre une difficulté technique. Un membre de notre équipe vous contactera bientôt."
        }

        try:
            # Vérifier que Ollama est accessible
            try:
                # Test de connexion à Ollama
                await asyncio.wait_for(
                    self.ollama_client.generate(
                        model=settings.ollama_model,
                        prompt="test",
                        stream=False
                    ),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                logger.error("Ollama timeout - service non disponible")
                return fallback_messages["error"]
            except Exception as conn_error:
                logger.error(f"Ollama connection error: {str(conn_error)}")
                return fallback_messages["error"]

            # Générer la réponse
            response = await asyncio.wait_for(
                self.ollama_client.generate(
                    model=settings.ollama_model,
                    prompt=full_prompt,
                    stream=False
                ),
                timeout=30.0  # Timeout de 30 secondes pour la génération
            )

            ai_response = response.get("response", "")
            
            # Vérifier que la réponse n'est pas vide
            if not ai_response or len(ai_response.strip()) < 5:
                logger.warning("Réponse IA vide ou trop courte")
                return fallback_messages["general"] if not context else fallback_messages["order"]

            logger.info(f"Réponse IA générée pour: {user_message[:50]}...")
            return ai_response.strip()

        except asyncio.TimeoutError:
            logger.error("Timeout lors de la génération de la réponse IA")
            return fallback_messages["error"]
        except ConnectionError as e:
            logger.error(f"Erreur de connexion Ollama: {str(e)}")
            return fallback_messages["error"]
        except Exception as e:
            logger.error(f"Erreur génération réponse IA: {str(e)}", exc_info=True)
            # Retourner un message de fallback contextuel
            if context:
                return fallback_messages["order"]
            return fallback_messages["general"]

    async def handle_incoming_message(
        self,
        from_number: str,
        message_text: str,
        message_id: str,
        db_session=None
    ) -> Dict[str, Any]:
        """
        Traite un message entrant et génère une réponse

        Retourne: Dict avec la réponse à envoyer
        """
        logger.info(f"Message reçu de {from_number}: {message_text[:50]}...")

        # Récupérer le contexte de la commande si disponible
        context = None
        if db_session:
            try:
                from sqlalchemy import select, desc
                from app.models.orders import Order
                
                # Récupérer la commande la plus récente pour ce numéro
                result = await db_session.execute(
                    select(Order)
                    .where(Order.phone == from_number)
                    .order_by(desc(Order.created_at))
                    .limit(1)
                )
                order = result.scalar_one_or_none()
                
                if order:
                    context = {
                        "order_id": order.id,
                        "product_name": order.product_name,
                        "status": order.status,
                        "quantity": order.quantity,
                        "created_at": order.created_at.isoformat() if order.created_at else None
                    }
                    logger.info(f"Contexte commande récupéré: Commande #{order.id} - {order.product_name}")
                else:
                    logger.debug(f"Aucune commande trouvée pour {from_number}")
                    
            except Exception as e:
                logger.warning(f"Erreur récupération contexte commande: {str(e)}", exc_info=True)
                # Continuer sans contexte si erreur

        # Générer la réponse IA
        ai_response = await self.generate_ai_response(message_text, context)

        # Envoyer la réponse
        try:
            result = await self.send_message(
                to=from_number,
                message=ai_response
            )

            return {
                "status": "sent",
                "message_id": result.get("messages", [{}])[0].get("id"),
                "response": ai_response
            }

        except Exception as e:
            logger.error(f"Erreur envoi réponse: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

