import uuid
from typing import Any

from httpx import AsyncClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.business import Business
from app.models.courts import Court
from app.models.match_extended import MatchExtended, MatchPlayer
from app.models.mercadopago_payment import MercadoPagoPaymentCreate
from app.models.payment import PaymentCreate, PaymentStatus
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.repository.payments_repository import PaymentsRepository
from app.services.business_service import BusinessService
from app.services.matches_service import MatchesService
from app.services.mercadopago_service import MercadoPagoService
from app.services.payments_service import PaymentsService


async def test_create_match_payment_returns_payment_data(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    class test_data:
        user_public_id = str(uuid.uuid4())
        match_public_id = str(uuid.uuid4())
        business_public_id = str(uuid.uuid4())
        business_name = "Business Name"
        court_public_id = str(uuid.uuid4())
        court_price = 40_000
        time = 9
        date = "2025-05-01"
        preference_id = str(uuid.uuid4())
        pay_url = (
            f"https://www.mercadopago.com/mla/checkout/start?pref_id={preference_id}"
        )

    payload = {
        "user_public_id": test_data.user_public_id,
        "match_public_id": test_data.match_public_id,
    }

    async def mock_get_player_match(
        self: Any,  # noqa: ARG001
        user_public_id: uuid.UUID,  # noqa: ARG001
        match_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return MatchExtended(
            public_id=test_data.match_public_id,
            court_public_id=test_data.court_public_id,
            date=test_data.date,
            time=test_data.time,
            match_players=[
                MatchPlayer(
                    user_public_id=test_data.user_public_id,
                    match_public_id=test_data.match_public_id,
                )
            ],
        )

    monkeypatch.setattr(MatchesService, "get_player_match", mock_get_player_match)

    async def mock_get_court(
        self: Any,  # noqa: ARG001
        court_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return Court(
            court_public_id=test_data.court_public_id,
            business_public_id=test_data.business_public_id,
            price_per_hour=test_data.court_price,
        )

    monkeypatch.setattr(BusinessService, "get_court", mock_get_court)

    async def mock_get_business(
        self: Any,  # noqa: ARG001
        business_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return Business(
            business_public_id=test_data.business_public_id,
            name=test_data.business_name,
        )

    monkeypatch.setattr(BusinessService, "get_business", mock_get_business)

    def mock_create_preference(
        self: Any,  # noqa: ARG001
        preference_data: dict[str, Any],  # noqa: ARG001
    ) -> Any:
        preference_response = {
            "response": {
                "id": test_data.preference_id,
                "init_point": test_data.pay_url,
            }
        }
        return preference_response

    monkeypatch.setattr(MercadoPagoService, "create_preference", mock_create_preference)

    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/",
        headers=x_api_key_header,
        json=payload,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["public_id"] is not None
    assert content["match_public_id"] == test_data.match_public_id
    assert content["user_public_id"] == test_data.user_public_id
    assert content["amount"] == test_data.court_price / PaymentsService.N_PLAYERS
    assert content["pay_url"] == test_data.pay_url


async def test_create_match_payment_stores_payment_data(
    session: AsyncSession,
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    monkeypatch: Any,
) -> None:
    class test_data:
        user_public_id = str(uuid.uuid4())
        match_public_id = str(uuid.uuid4())
        business_public_id = str(uuid.uuid4())
        business_name = "Business Name"
        court_public_id = str(uuid.uuid4())
        court_price = 40_000
        time = 9
        date = "2025-05-01"
        preference_id = str(uuid.uuid4())
        pay_url = (
            f"https://www.mercadopago.com/mla/checkout/start?pref_id={preference_id}"
        )

    payload = {
        "user_public_id": test_data.user_public_id,
        "match_public_id": test_data.match_public_id,
    }

    async def mock_get_player_match(
        self: Any,  # noqa: ARG001
        user_public_id: uuid.UUID,  # noqa: ARG001
        match_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return MatchExtended(
            public_id=test_data.match_public_id,
            court_public_id=test_data.court_public_id,
            date=test_data.date,
            time=test_data.time,
            match_players=[
                MatchPlayer(
                    user_public_id=test_data.user_public_id,
                    match_public_id=test_data.match_public_id,
                )
            ],
        )

    monkeypatch.setattr(MatchesService, "get_player_match", mock_get_player_match)

    async def mock_get_court(
        self: Any,  # noqa: ARG001
        court_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return Court(
            court_public_id=test_data.court_public_id,
            business_public_id=test_data.business_public_id,
            price_per_hour=test_data.court_price,
        )

    monkeypatch.setattr(BusinessService, "get_court", mock_get_court)

    async def mock_get_business(
        self: Any,  # noqa: ARG001
        business_public_id: uuid.UUID,  # noqa: ARG001
    ) -> Any:
        return Business(
            business_public_id=test_data.business_public_id,
            name=test_data.business_name,
        )

    monkeypatch.setattr(BusinessService, "get_business", mock_get_business)

    def mock_create_preference(
        self: Any,  # noqa: ARG001
        preference_data: dict[str, Any],  # noqa: ARG001
    ) -> Any:
        preference_response = {
            "response": {"id": test_data.preference_id, "init_point": test_data.pay_url}
        }
        return preference_response

    monkeypatch.setattr(MercadoPagoService, "create_preference", mock_create_preference)

    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/",
        headers=x_api_key_header,
        json=payload,
    )
    assert response.status_code == 201

    content = response.json()
    payment_public_id = content["public_id"]
    payment_url = content["pay_url"]

    pref_id = payment_url.split("pref_id=")[1]
    assert pref_id == test_data.preference_id

    pay_repo = PaymentsRepository(session)
    payment = await pay_repo.get_payment(public_id=payment_public_id)
    assert str(payment.public_id) == payment_public_id
    assert str(payment.match_public_id) == test_data.match_public_id
    assert str(payment.user_public_id) == test_data.user_public_id
    assert payment.amount == test_data.court_price / PaymentsService.N_PLAYERS
    assert payment.status == PaymentStatus.PENDING

    mp_pay_repo = MercadoPagoPaymentsRepository(session)
    mp_payment = await mp_pay_repo.get_payment(public_id=payment_public_id)
    assert str(mp_payment.public_id) == payment_public_id
    assert mp_payment.preference_id == test_data.preference_id
    assert mp_payment.pay_url == test_data.pay_url


async def test_create_match_payment_returns_same_payment_data_if_status_pending(
    session: AsyncSession, async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    class test_data:
        user_public_id = str(uuid.uuid4())
        match_public_id = str(uuid.uuid4())
        amount = 20_000
        preference_id = str(uuid.uuid4())
        pay_url = "https://this-is-a-pay-url.com"

    payload = {
        "user_public_id": test_data.user_public_id,
        "match_public_id": test_data.match_public_id,
    }
    payment = await PaymentsRepository(session).create_payment(
        PaymentCreate(
            user_public_id=test_data.user_public_id,
            match_public_id=test_data.match_public_id,
            amount=test_data.amount,
        ),
        should_commit=True,
    )
    _mp_payment = await MercadoPagoPaymentsRepository(session).create_payment(
        MercadoPagoPaymentCreate(
            public_id=payment.public_id,
            preference_id=test_data.preference_id,
            pay_url=test_data.pay_url,
        ),
        should_commit=True,
    )
    assert payment.status == PaymentStatus.PENDING

    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/",
        headers=x_api_key_header,
        json=payload,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["public_id"] == str(payment.public_id)
    assert content["match_public_id"] == test_data.match_public_id
    assert content["user_public_id"] == test_data.user_public_id
    assert content["amount"] == test_data.amount
    assert content["pay_url"] == test_data.pay_url
    assert content["status"] == PaymentStatus.PENDING
