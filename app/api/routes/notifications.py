import logging
from typing import Any

from fastapi import APIRouter, Request, Response, status

from app.core.config import settings
from app.services.mercado_pago_service import MercadoPagoNotificationService

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
    default_response = Response(status_code=status.HTTP_200_OK)

    MercadoPagoNotificationService().verify_request(request)

    body = await request.json()

    ressource_id = body["data"]["id"]
    if ressource_id == settings.MERCADO_PAGO_NOTIFICATION_TEST_ID:
        return default_response

    notification_type = body["type"]

    merchant_order_id = None
    if notification_type == "topic_merchant_order_wh":
        merchant_order_id = ressource_id
    elif notification_type == "payment":
        payment_response = mp_sdk.payment().get(ressource_id)
        payment = payment_response["response"]
        merchant_order_id = payment["order"]["id"]
    else:
        logger.info(f"{request.query_params = }")
        logger.info(f"{request.headers = }")
        logger.info(f"{await request.json() = }")

    if merchant_order_id:
        merchant_order_response = mp_sdk.merchant_order().get(merchant_order_id)
        merchant_order = merchant_order_response["response"]

        total_paid = 0
        for payment in merchant_order["payments"]:
            if payment["status"] == "approved":
                total_paid += payment["transaction_amount"]

        item_title = merchant_order["items"][0]["title"]
        if total_paid >= merchant_order["total_amount"]:
            logger.info(f"[Merchant Order] '{item_title}': DONE")
        else:
            logger.info(f"[Merchant Order] '{item_title}': WIP")

    return default_response
