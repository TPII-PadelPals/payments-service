from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.mercado_pago_payment import MercadoPagoPayment, MercadoPagoPaymentCreate
from app.utilities.exceptions import NotFoundException


class MercadoPagoPaymentsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_payment(
        self, payment_create: MercadoPagoPaymentCreate
    ) -> MercadoPagoPayment:
        payment = MercadoPagoPayment.model_validate(payment_create)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_payments(self, **filters: Any) -> list[MercadoPagoPayment]:
        query = select(MercadoPagoPayment)
        for key, value in filters.items():
            attr = getattr(MercadoPagoPayment, key)
            query = query.where(attr == value)
        result = await self.session.exec(query)
        payments = list(result.all())
        return payments

    async def get_payment(self, **filters: Any) -> MercadoPagoPayment:
        payments = await self.get_payments(**filters)
        if not payments:
            raise NotFoundException(f"MercadoPago Payment '{filters}'")
        return payments[0]
