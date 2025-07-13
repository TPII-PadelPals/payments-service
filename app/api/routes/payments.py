from typing import Any

from fastapi import APIRouter, status

from app.models.match_extended import MatchPlayer
from app.models.payment import PaymentExtendedPublic
from app.services.payments_service import PaymentsService
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post(
    "/",
    response_model=PaymentExtendedPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    session: SessionDep,
    match_player: MatchPlayer,
) -> Any:
    return await PaymentsService().create_payment(session, match_player)
