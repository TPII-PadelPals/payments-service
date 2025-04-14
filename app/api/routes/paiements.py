from typing import Any

from fastapi import APIRouter, status

from app.core.config import settings
from app.models.paiement import PaiementCreate, PaiementPublic

# from app.utilities.dependencies import SessionDep

mp_sdk = settings.MERCADO_PAGO_SDK

router = APIRouter()


@router.post(
    "/",
    response_model=PaiementPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_paiement(
    # session: SessionDep,
    paiement_in: PaiementCreate,
) -> Any:
    preference_data = {
        "items": [
            {
                "id": str(paiement_in.match_public_id),
                "title": paiement_in.match_title,
                "quantity": 1,
                "unit_price": paiement_in.amount,
            }
        ],
        "back_urls": {
            "success": f"https://web.telegram.org/a/#{paiement_in.user_telegram_id}",
            "pending": f"https://web.telegram.org/a/#{paiement_in.user_telegram_id}",
            "failure": f"https://web.telegram.org/a/#{paiement_in.user_telegram_id}",
        },
        "auto_return": "approved",
    }

    preference_response = mp_sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return PaiementPublic(url=preference["init_point"], **paiement_in.model_dump())
