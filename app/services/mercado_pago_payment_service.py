import logging

from app.core.config import settings
from app.models.business import Business
from app.models.match_extended import MatchExtended
from app.models.mercado_pago_payment import MercadoPagoPaymentCreate
from app.models.payment import PaymentCreate, PaymentPublic
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.repository.payments_repository import PaymentsRepository
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_sdk = settings.MERCADO_PAGO_SDK


class MercadoPagoPaymentService:
    N_PLAYERS = 4

    def get_payment_title(
        self, business: Business, match_extended: MatchExtended
    ) -> str:
        return f"PadelPals Match: {business.name} {match_extended.date} {match_extended.time}:00 hs"

    async def create_payment(
        self, session: SessionDep, match_extended: MatchExtended
    ) -> PaymentPublic:
        business_service = BusinessService()
        court = await business_service.get_court(match_extended.court_public_id)
        business = await business_service.get_business(court.business_public_id)

        payment_create = PaymentCreate(
            match_public_id=match_extended.public_id,
            user_public_id=match_extended.match_players[0].user_public_id,
            amount=(court.price_per_hour / self.N_PLAYERS),
        )

        repo_pay = PaymentsRepository(session)
        payment = await repo_pay.create_payment(payment_create)

        payment_title = self.get_payment_title(business, match_extended)

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

        preference_response = mp_sdk.preference().create(preference_data)
        preference = preference_response["response"]
        preference_id = preference["id"]
        preference_init_point = preference["init_point"]
        mp_payment_create = MercadoPagoPaymentCreate(
            public_id=payment.public_id, preference_id=preference_id
        )
        await MercadoPagoPaymentsRepository(session).create_payment(mp_payment_create)
        return PaymentPublic(pay_url=preference_init_point, **payment.model_dump())
