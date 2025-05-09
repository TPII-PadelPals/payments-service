import hashlib
import hmac
import logging
import urllib.parse

from fastapi import Request

from app.core.config import settings
from app.models.payment import PaymentStatus, PaymentUpdate
from app.repository.mercadopago_payments_repository import MercadoPagoPaymentsRepository
from app.repository.payments_repository import PaymentsRepository
from app.services.mercado_pago_service import MercadoPagoService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotAuthorizedException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_service = MercadoPagoService(settings.MERCADO_PAGO_SDK)


class MercadoPagoNotificationsService:
    def verify_request(self, request: Request) -> None:
        # Obtain the x-signature value from the header
        xSignature = request.headers.get("x-signature")
        xRequestId = request.headers.get("x-request-id")

        # Obtain Query params related to the request URL
        queryParams = urllib.parse.parse_qs(request.url.query)

        # Extract the "data.id" from the query params
        dataID = queryParams.get("data.id", [""])[0]

        # Separating the x-signature into parts
        parts = xSignature.split(",")  # type: ignore

        # Initializing variables to store ts and hash
        ts = None
        hash = None

        # Iterate over the values to obtain ts and v1
        for part in parts:
            # Split each part into key and value
            keyValue = part.split("=", 1)
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == "ts":
                    ts = value
                elif key == "v1":
                    hash = value

        # Obtain the secret key for the user/application from Mercadopago developers site
        secret = settings.MERCADO_PAGO_NOTIFICATION_SECRET_KEY

        # Generate the manifest string
        manifest = f"id:{dataID};request-id:{xRequestId};ts:{ts};"

        # Create an HMAC signature defining the hash type and the key as a byte array
        hmac_obj = hmac.new(
            secret.encode(), msg=manifest.encode(), digestmod=hashlib.sha256
        )

        # Obtain the hash result as a hexadecimal string
        sha = hmac_obj.hexdigest()
        if sha != hash:
            # HMAC verification failed
            raise NotAuthorizedException()

    async def process_request(self, session: SessionDep, request: Request) -> None:
        self.verify_request(request)

        body = await request.json()

        ressource_id = body["data"]["id"]
        if ressource_id == settings.MERCADO_PAGO_NOTIFICATION_TEST_ID:
            return

        notification_type = body["type"]

        merchant_order_id = None
        if notification_type == "topic_merchant_order_wh":
            merchant_order_id = ressource_id
        elif notification_type == "payment":
            payment_response = mp_service.get_payment(ressource_id)
            payment = payment_response["response"]
            merchant_order_id = payment["order"]["id"]
        else:
            logger.info(f"{request.query_params = }")
            logger.info(f"{request.headers = }")
            logger.info(f"{await request.json() = }")

        if merchant_order_id:
            merchant_order_response = mp_service.get_merchant_order(merchant_order_id)
            merchant_order = merchant_order_response["response"]
            if merchant_order["status"] == "closed":
                preference_id = merchant_order["preference_id"]
                mp_payment = await MercadoPagoPaymentsRepository(session).get_payment(
                    preference_id=preference_id
                )
                payment_update = PaymentUpdate(status=PaymentStatus.PAID)
                await PaymentsRepository(session).update_payment(
                    mp_payment.public_id, payment_update
                )

        # total_paid = 0
        # for payment in merchant_order["payments"]:
        #     if payment["status"] == "approved":
        #         total_paid += payment["transaction_amount"]

        # item_title = merchant_order["items"][0]["title"]
        # if total_paid >= merchant_order["total_amount"]:
        #     logger.info(f"[Merchant Order] '{item_title}': DONE")
        # else:
        #     logger.info(f"[Merchant Order] '{item_title}': WIP")
