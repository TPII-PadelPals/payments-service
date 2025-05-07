from typing import Any

from fastapi import APIRouter, status

from app.models.match_extended import MatchExtended
from app.models.payment import PaymentPublic
from app.services.mercado_pago_payment_service import MercadoPagoPaymentService
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post(
    "/",
    response_model=PaymentPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    session: SessionDep,
    match_extended: MatchExtended,
) -> Any:
    return await MercadoPagoPaymentService().create_payment(session, match_extended)
