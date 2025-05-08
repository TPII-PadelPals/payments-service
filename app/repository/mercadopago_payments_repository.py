from uuid import UUID

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

    async def get_payment(self, public_id: UUID) -> MercadoPagoPayment:
        query = select(MercadoPagoPayment).where(
            MercadoPagoPayment.public_id == public_id
        )
        result = await self.session.exec(query)
        payment = result.first()
        if payment is None:
            raise NotFoundException(f"MercadoPago Payment '{public_id}'")
        return payment
