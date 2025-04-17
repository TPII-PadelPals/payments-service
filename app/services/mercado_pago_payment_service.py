import logging

from app.core.config import settings
from app.models.payment import PaymentCreate, PaymentPublic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_sdk = settings.MERCADO_PAGO_SDK


class MercadoPagoPaymentService:
    def create_payment(self, payment_in: PaymentCreate) -> PaymentPublic:
        preference_data = {
            "items": [
                {
                    "id": str(payment_in.match_public_id),
                    "title": payment_in.match_title,
                    "quantity": 1,
                    "unit_price": payment_in.amount,
                }
            ],
            "back_urls": {
                "success": f"https://web.telegram.org/a/#{payment_in.user_telegram_id}",
                "pending": f"https://web.telegram.org/a/#{payment_in.user_telegram_id}",
                "failure": f"https://web.telegram.org/a/#{payment_in.user_telegram_id}",
            },
            "auto_return": "approved",
        }

        preference_response = mp_sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return PaymentPublic(url=preference["init_point"], **payment_in.model_dump())
