import logging
from typing import Any

from app.core.config import settings
from app.models.business import Business
from app.models.match_extended import MatchExtended
from app.models.mercadopago_payment import (
    MercadoPagoPayment,
    MercadoPagoPaymentCreate,
    MercadoPagoPaymentExtended,
)
from app.models.payment import Payment
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.services.mercadopago_service import MercadoPagoService
from app.utilities.dependencies import SessionDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MercadoPagoPaymentsService:
    mp_service = MercadoPagoService(settings.MERCADO_PAGO_SDK)

    def get_payment_title(
        self, business: Business, match_extended: MatchExtended
    ) -> str:
        return f"PadelPals Match: {business.name} {match_extended.date} {match_extended.time}:00 hs"

    async def create_payment(
        self,
        session: SessionDep,
        payment: Payment,
        payment_title: str,
        should_commit: bool = True,
    ) -> MercadoPagoPaymentExtended:
        preference_data = {
            "items": [
                {
                    "id": str(payment.public_id),
                    "title": payment_title,
                    "quantity": 1,
                    "unit_price": payment.amount,
                }
            ],
            "back_urls": {
                "success": settings.BOT_URL,
                "pending": settings.BOT_URL,
                "failure": settings.BOT_URL,
            },
            "auto_return": "approved",
        }

        preference_response = self.mp_service.create_preference(preference_data)
        preference = preference_response["response"]
        preference_id = preference["id"]
        preference_init_point = preference["init_point"]
        mp_payment_create = MercadoPagoPaymentCreate(
            public_id=payment.public_id, preference_id=preference_id
        )
        mp_payment = await MercadoPagoPaymentsRepository(session).create_payment(
            mp_payment_create, should_commit
        )

        return MercadoPagoPaymentExtended(
            pay_url=preference_init_point, **mp_payment.model_dump()
        )

    async def get_payment(
        self, session: SessionDep, **filters: Any
    ) -> MercadoPagoPayment:
        return await MercadoPagoPaymentsRepository(session).get_payment(**filters)
