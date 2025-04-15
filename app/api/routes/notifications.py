from typing import Any

from fastapi import APIRouter, Request, Response, status

from app.core.config import settings
from app.services.mercado_pago_notifications_service import (
    MercadoPagoNotificationsService,
)

mp_sdk = settings.MERCADO_PAGO_SDK

router = APIRouter()


@router.post(
    "/mercadopago",
    status_code=status.HTTP_200_OK,
)
async def mercadopago_notify(
    request: Request,
) -> Any:
    await MercadoPagoNotificationsService().process_request(request)
    return Response(status_code=status.HTTP_200_OK)
