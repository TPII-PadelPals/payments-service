from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.payment import Payment, PaymentCreate
from app.utilities.exceptions import NotFoundException


class PaymentsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_payment(self, payment_create: PaymentCreate) -> Payment:
        payment = Payment.model_validate(payment_create)
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def get_payment(self, public_id: UUID) -> Payment:
        query = select(Payment).where(Payment.public_id == public_id)
        result = await self.session.exec(query)
        payment = result.first()
        if payment is None:
            raise NotFoundException(f"Payment '{public_id}'")
        return payment
