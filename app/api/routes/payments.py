from typing import Any

from fastapi import APIRouter, status

from app.models.match_extended import MatchExtended
from app.models.payment import PaymentExtendedPublic
from app.services.payment_service import PaymentService
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post(
    "/",
    response_model=PaymentExtendedPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    session: SessionDep,
    match_extended: MatchExtended,
) -> Any:
    return await PaymentService().create_payment(session, match_extended)
