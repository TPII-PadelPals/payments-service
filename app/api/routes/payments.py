from typing import Any

from fastapi import APIRouter, status

from app.core.config import settings
from app.models.payment import PaymentCreate, PaymentPublic
from app.services.mercado_pago_payment_service import MercadoPagoPaymentService

mp_sdk = settings.MERCADO_PAGO_SDK

router = APIRouter()


@router.post(
    "/",
    response_model=PaymentPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    payment_in: PaymentCreate,
) -> Any:
    return MercadoPagoPaymentService().create_payment(payment_in)
