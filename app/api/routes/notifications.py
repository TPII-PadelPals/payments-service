from typing import Any

from fastapi import APIRouter, Request, Response, status

from app.services.mercadopago_notifications_service import (
    MercadoPagoNotificationsService,
)
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post(
    "/mercadopago",
    status_code=status.HTTP_200_OK,
)
async def mercadopago_notify(session: SessionDep, request: Request) -> Any:
    await MercadoPagoNotificationsService().process_request(session, request)
    return Response(status_code=status.HTTP_200_OK)
