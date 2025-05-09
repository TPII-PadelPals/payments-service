import uuid
from typing import Any

from fastapi import Request
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.mercado_pago_payment import MercadoPagoPaymentCreate
from app.models.payment import PaymentCreate, PaymentStatus
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.repository.payments_repository import PaymentsRepository
from app.services.mercado_pago_notifications_service import (
    MercadoPagoNotificationsService,
)
from app.services.mercado_pago_service import MercadoPagoService

mp_sdk = settings.MERCADO_PAGO_SDK


async def test_notification_merchant_order_closed_sets_payment_status_paid(
    session: AsyncSession,
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    monkeypatch: Any,
) -> None:
    payment_preference_id = str(uuid.uuid4())

    PayRepo = PaymentsRepository(session)
    payment = await PayRepo.create_payment(
        PaymentCreate(
            match_public_id=str(uuid.uuid4()),
            user_public_id=str(uuid.uuid4()),
            amount=10_000,
        )
    )
    MPPayRepo = MercadoPagoPaymentsRepository(session)
    await MPPayRepo.create_payment(
        MercadoPagoPaymentCreate(
            public_id=payment.public_id, preference_id=payment_preference_id
        )
    )

    merchant_order_id = 2222_2222
    merchant_order = {"preference_id": payment_preference_id, "status": "closed"}
    merchant_order_response = {"response": merchant_order}

    def mock_get_merchant_order(_self: Any, _merchant_order_id: int) -> Any:
        if _merchant_order_id == merchant_order_id:
            return merchant_order_response
        return None

    monkeypatch.setattr(
        MercadoPagoService, "get_merchant_order", mock_get_merchant_order
    )

    def mock_verify_request(_self: Any, _request: Request) -> None:
        pass

    monkeypatch.setattr(
        MercadoPagoNotificationsService, "verify_request", mock_verify_request
    )

    notification = {
        "type": "topic_merchant_order_wh",
        "data": {"id": merchant_order_id},
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/notifications/mercadopago",
        headers=x_api_key_header,
        json=notification,
    )
    assert response.status_code == 200

    result_payment = await PayRepo.get_payment(payment.public_id)
    assert result_payment.status == PaymentStatus.PAID
