import uuid
from typing import Any

from httpx import AsyncClient

from app.core.config import settings
from app.models.business import Business
from app.models.courts import Court
from app.services.business_service import BusinessService

# mp_sdk = settings.MERCADO_PAGO_SDK


async def test_create_match_payment(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    match_public_id = str(uuid.uuid4())
    user_public_id = str(uuid.uuid4())
    business_public_id = str(uuid.uuid4())
    business_name = "Business Name"
    court_public_id = str(uuid.uuid4())
    court_price = 40_000
    payload = {
        "public_id": match_public_id,
        "court_public_id": court_public_id,
        "date": "2025-05-01",
        "time": 9,
        "match_players": [
            {"match_public_id": match_public_id, "user_public_id": user_public_id}
        ],
    }

    async def mock_get_court(
        self: Any,  # noqa: ARG001
        court_public_id: uuid.UUID,
    ) -> Any:
        return Court(
            court_public_id=court_public_id,
            business_public_id=business_public_id,
            price_per_hour=court_price,
        )

    monkeypatch.setattr(BusinessService, "get_court", mock_get_court)

    async def mock_get_business(
        self: Any,  # noqa: ARG001
        business_public_id: uuid.UUID,
    ) -> Any:
        return Business(business_public_id=business_public_id, name=business_name)

    monkeypatch.setattr(BusinessService, "get_business", mock_get_business)

    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/",
        headers=x_api_key_header,
        json=payload,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["match_public_id"] == match_public_id
    assert content["user_public_id"] == user_public_id
    assert content["amount"] == 10_000
    assert content["pay_url"] is not None
