from typing import Any

from sqlalchemy.exc import IntegrityError

from app.models.payment import Payment, PaymentCreate, PaymentUpdate
from app.repository.base_repository import BaseRepository
from app.utilities.exceptions import NotUniqueException


class PaymentsRepository(BaseRepository):
    def _handle_commit_exceptions(self, err: IntegrityError) -> None:
        if "uq_user_match_constraint" in str(err.orig):
            raise NotUniqueException("Payment")
        else:
            raise err

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
