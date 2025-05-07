import logging
import uuid

from app.core.config import settings
from app.models.match_extended import MatchExtended
from app.models.payment import PaymentPublic
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_sdk = settings.MERCADO_PAGO_SDK


class MercadoPagoPaymentService:
    async def create_payment(
        self, session: SessionDep, match_extended: MatchExtended
    ) -> PaymentPublic:
        business_service = BusinessService()
        court = await business_service.get_court(match_extended.court_public_id)
        business = await business_service.get_business(court.business_public_id)

        payment_data = {
            "match_public_id": match_extended.public_id,
            "user_public_id": match_extended.match_players[0].user_public_id,
            "public_id": str(uuid.uuid4()),
            "title": f"PadelPals Match: {business.name} {match_extended.date} {match_extended.time}:00 hs",
            "amount": court.price_per_hour / 4,
        }

        preference_data = {
            "items": [
                {
                    "id": payment_data["public_id"],
                    "title": payment_data["title"],
                    "quantity": 1,
                    "unit_price": payment_data["amount"],
                }
            ],
            "back_urls": {
                "success": settings.BOT_URL,
                "pending": settings.BOT_URL,
                "failure": settings.BOT_URL,
            },
            "auto_return": "approved",
        }

        preference_response = mp_sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return PaymentPublic(pay_url=preference["init_point"], **payment_data)
