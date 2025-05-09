from typing import Any

from app.models.payment import Payment, PaymentCreate, PaymentUpdate
from app.repository.base_repository import BaseRepository


class PaymentsRepository(BaseRepository):
    async def create_payment(
        self, payment_create: PaymentCreate, should_commit: bool = True
    ) -> Payment:
        return await self.create_record(Payment, payment_create, should_commit)

    async def get_payment(self, **filters: Any) -> Payment:
        return await self.get_record(Payment, **filters)

    async def update_payment(
        self, payment_update: PaymentUpdate, should_commit: bool = True, **filters: Any
    ) -> Payment:
        return await self.update_record(
            Payment, payment_update, should_commit, **filters
        )
