import logging
from typing import Any

from fastapi import APIRouter, Request, Response, status

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_sdk = settings.MERCADO_PAGO_SDK

router = APIRouter()


@router.post(
    "/mercadopago",
    status_code=status.HTTP_200_OK,
)
async def mercadopago_notify(
    request: Request,
) -> Any:
    logger.info(request)
    return Response(status_code=status.HTTP_200_OK)
