import uuid
from typing import Any

from fastapi import APIRouter, status

from app.core.config import settings

# from app.utilities.dependencies import SessionDep

mp_sdk = settings.MERCADO_PAGO_SDK

router = APIRouter()


@router.post(
    "/",
    # response_model=ItemsPublic,
    status_code=status.HTTP_200_OK,
    # responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
    # dependencies=[Depends(get_user_id_param)],
)
async def create_paiement(
    # session: SessionDep,
    match_public_id: uuid.UUID,
    match_title: str,
    amount: float,
    telegram_id: int,
) -> Any:
    preference_data = {
        "items": [
            {
                "id": match_public_id,
                "title": match_title,
                "quantity": 1,
                "unit_price": amount,
            }
        ],
        "back_urls": {
            "success": f"https://web.telegram.org/a/#{telegram_id}",
            "pending": f"https://web.telegram.org/a/#{telegram_id}",
            "failure": f"https://web.telegram.org/a/#{telegram_id}",
        },
        "notification_url": "https://localhost:8004/notifications/mercadopago",
        "auto_return": "approved",
    }

    preference_response = mp_sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return {
        "match_public_id": match_public_id,
        "match_title": match_title,
        "amount": amount,
        "telegram_id": telegram_id,
        "paiement_url": preference.body.init_point,
    }
