import uuid
from typing import Any

from fastapi import Request
from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.mercadopago_payment import MercadoPagoPaymentCreate
from app.models.payment import PaymentCreate, PaymentStatus
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.repository.payments_repository import PaymentsRepository
from app.services.mercadopago_notifications_service import (
    MercadoPagoNotificationsService,
)
from app.services.mercadopago_service import MercadoPagoService


async def test_notification_merchant_order_opened_leaves_payment_status_pending(
    session: AsyncSession,
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    monkeypatch: Any,
) -> None:
    payment_preference_id = str(uuid.uuid4())
    pay_url = f"https://www.mercadopago.com/mla/checkout/start?pref_id={payment_preference_id}"

    pay_repo = PaymentsRepository(session)
    payment = await pay_repo.create_payment(
        PaymentCreate(
            match_public_id=str(uuid.uuid4()),
            user_public_id=str(uuid.uuid4()),
            amount=10_000,
        )
    )
    mp_pay_repo = MercadoPagoPaymentsRepository(session)
    await mp_pay_repo.create_payment(
        MercadoPagoPaymentCreate(
            public_id=payment.public_id,
            preference_id=payment_preference_id,
            pay_url=pay_url,
        )
    )

    # Mock mercadopago merchant_order
    merchant_order_id = 1111_1111
    merchant_order_json = {
        "response": {"preference_id": payment_preference_id, "status": "opened"}
    }

    def mock_get_merchant_order(_self: Any, _merchant_order_id: int) -> Any:
        if _merchant_order_id == merchant_order_id:
            return merchant_order_json
        return None

    monkeypatch.setattr(
        MercadoPagoService, "get_merchant_order", mock_get_merchant_order
    )

    # Mock mercadopago verification
    def mock_verify_request(_self: Any, _request: Request) -> None:
        pass

    monkeypatch.setattr(
        MercadoPagoNotificationsService, "verify_request", mock_verify_request
    )

    # Test merchant_order notification
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

    result_payment = await pay_repo.get_payment(public_id=payment.public_id)
    assert result_payment.status == PaymentStatus.PENDING


async def test_notification_merchant_order_closed_sets_payment_status_paid(
    session: AsyncSession,
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    monkeypatch: Any,
) -> None:
    payment_preference_id = str(uuid.uuid4())
    pay_url = f"https://www.mercadopago.com/mla/checkout/start?pref_id={payment_preference_id}"

    pay_repo = PaymentsRepository(session)
    payment = await pay_repo.create_payment(
        PaymentCreate(
            match_public_id=str(uuid.uuid4()),
            user_public_id=str(uuid.uuid4()),
            amount=10_000,
        )
    )
    mp_pay_repo = MercadoPagoPaymentsRepository(session)
    await mp_pay_repo.create_payment(
        MercadoPagoPaymentCreate(
            public_id=payment.public_id,
            preference_id=payment_preference_id,
            pay_url=pay_url,
        )
    )

    # Mock mercadopago merchant_order
    merchant_order_id = 1111_1111
    merchant_order_json = {
        "response": {"preference_id": payment_preference_id, "status": "closed"}
    }

    def mock_get_merchant_order(_self: Any, _merchant_order_id: int) -> Any:
        if _merchant_order_id == merchant_order_id:
            return merchant_order_json
        return None

    monkeypatch.setattr(
        MercadoPagoService, "get_merchant_order", mock_get_merchant_order
    )

    # Mock mercadopago verification
    def mock_verify_request(_self: Any, _request: Request) -> None:
        pass

    monkeypatch.setattr(
        MercadoPagoNotificationsService, "verify_request", mock_verify_request
    )

    # Test merchant_order notification
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

    result_payment = await pay_repo.get_payment(public_id=payment.public_id)
    assert result_payment.status == PaymentStatus.PAID


async def test_notification_payment_merchant_order_closed_sets_payment_status_paid(
    session: AsyncSession,
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    monkeypatch: Any,
) -> None:
    payment_preference_id = str(uuid.uuid4())
    pay_url = f"https://www.mercadopago.com/mla/checkout/start?pref_id={payment_preference_id}"

    pay_repo = PaymentsRepository(session)
    payment = await pay_repo.create_payment(
        PaymentCreate(
            match_public_id=str(uuid.uuid4()),
            user_public_id=str(uuid.uuid4()),
            amount=10_000,
        )
    )
    mp_pay_repo = MercadoPagoPaymentsRepository(session)
    await mp_pay_repo.create_payment(
        MercadoPagoPaymentCreate(
            public_id=payment.public_id,
            preference_id=payment_preference_id,
            pay_url=pay_url,
        )
    )

    # Mock mercadopago merchant_order
    merchant_order_id = 1111_1111
    merchant_order_json = {
        "response": {"preference_id": payment_preference_id, "status": "closed"}
    }

    def mock_get_merchant_order(_self: Any, _merchant_order_id: int) -> Any:
        if _merchant_order_id == merchant_order_id:
            return merchant_order_json
        return None

    monkeypatch.setattr(
        MercadoPagoService, "get_merchant_order", mock_get_merchant_order
    )

    # Mock mercadopago payment
    payment_id = 2222_2222
    payment_json = {"response": {"order": {"id": merchant_order_id}}}

    def mock_get_payment(_self: Any, _payment_id: int) -> Any:
        if _payment_id == payment_id:
            return payment_json
        return None

    monkeypatch.setattr(MercadoPagoService, "get_payment", mock_get_payment)

    # Mock mercadopago verification
    def mock_verify_request(_self: Any, _request: Request) -> None:
        pass

    monkeypatch.setattr(
        MercadoPagoNotificationsService, "verify_request", mock_verify_request
    )

    # Test payment notification
    notification = {
        "type": "payment",
        "data": {"id": payment_id},
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/notifications/mercadopago",
        headers=x_api_key_header,
        json=notification,
    )
    assert response.status_code == 200

    result_payment = await pay_repo.get_payment(public_id=payment.public_id)
    assert result_payment.status == PaymentStatus.PAID
