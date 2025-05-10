import logging
from typing import Any

from app.core.config import settings
from app.models.business import Business
from app.models.courts import Court
from app.models.match_extended import MatchExtended
from app.models.payment import Payment, PaymentCreate, PaymentExtended, PaymentUpdate
from app.repository.payments_repository import PaymentsRepository
from app.services.business_service import BusinessService
from app.services.mercadopago_payments_service import MercadoPagoPaymentsService
from app.utilities.dependencies import SessionDep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_sdk = settings.MERCADO_PAGO_SDK


class PaymentsService:
    N_PLAYERS = 4

    def get_payment_title(
        self, business: Business, match_extended: MatchExtended
    ) -> str:
        return f"PadelPals Match: {business.name} {match_extended.date} {match_extended.time}:00 hs"

    async def _create_payment(
        self,
        session: SessionDep,
        match_extended: MatchExtended,
        court: Court,
        should_commit: bool = True,
    ) -> Payment:
        payment_create = PaymentCreate(
            match_public_id=match_extended.public_id,
            user_public_id=match_extended.match_players[0].user_public_id,
            amount=(court.price_per_hour / self.N_PLAYERS),
        )

        payment = await PaymentsRepository(session).create_payment(
            payment_create, should_commit
        )

        return payment

    async def create_payment(
        self, session: SessionDep, match_extended: MatchExtended
    ) -> PaymentExtended:
        try:
            business_service = BusinessService()
            court = await business_service.get_court(match_extended.court_public_id)
            business = await business_service.get_business(court.business_public_id)

            payment_title = self.get_payment_title(business, match_extended)

            payment = await self._create_payment(
                session, match_extended, court, should_commit=False
            )

            mp_payment = await MercadoPagoPaymentsService().create_payment(
                session, payment, payment_title, should_commit=False
            )

            await session.commit()
        except Exception as err:
            await session.rollback()
            raise err

        return PaymentExtended(pay_url=mp_payment.pay_url, **payment.model_dump())

    async def update_payment(
        self, session: SessionDep, payment_update: PaymentUpdate, **filters: Any
    ) -> Payment:
        return await PaymentsRepository(session).update_payment(
            payment_update, **filters
        )
