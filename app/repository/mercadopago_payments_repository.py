from typing import Any

from app.models.mercado_pago_payment import MercadoPagoPayment, MercadoPagoPaymentCreate
from app.repository.base_repository import BaseRepository


class MercadoPagoPaymentsRepository(BaseRepository):
    async def create_payment(
        self, payment_create: MercadoPagoPaymentCreate, should_commit: bool = True
    ) -> MercadoPagoPayment:
        return await self.create_record(
            MercadoPagoPayment, payment_create, should_commit
        )

    async def get_payment(self, **filters: Any) -> MercadoPagoPayment:
        return await self.get_record(MercadoPagoPayment, **filters)
