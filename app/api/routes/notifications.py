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
    MercadoPagoNotificationService().verify_request(request)

    body = await request.json()
    notification_type = body["type"]
    if notification_type == "payment":
        payment_id = body["data"]["id"]
        payment_response = mp_sdk.payment().get(payment_id)
        payment = payment_response["response"]

        logger.info(f"{payment = }")
        """
        payment = {'status': 200, 'response': {'accounts_info': None, 'acquirer_reconciliation': [], 'additional_info': {'ip_address': '181.171.9.247', 'items': [{'id': '3fa85f64-5717-4562-b3fc-2c963f66afb2', 'quantity': '1', 'title': 'PadelPals 6h14', 'unit_price': '1000'}], 'tracking_id': 'platform:v1-blacklabel,so:ALL,type:N/A,security:none'}, 'authorization_code': None, 'binary_mode': False, 'brand_id': None, 'build_version': '3.100.0-rc-15', 'call_for_authorize_id': None, 'captured': True, 'card': {}, 'charges_details': [{'accounts': {'from': 'collector', 'to': 'mp'}, 'amounts': {'original': 41, 'refunded': 0}, 'client_id': 0, 'date_created': '2025-04-14T17:15:11.000-04:00', 'id': '108418929904-001', 'last_updated': '2025-04-14T17:15:11.000-04:00', 'metadata': {'source': 'rule-engine'}, 'name': 'mercadopago_fee', 'refund_charges': [], 'reserve_id': None, 'type': 'fee'}], 'charges_execution_info': {'internal_execution': {'date': '2025-04-14T17:15:11.934-04:00', 'execution_id': '01JRV2FYM1NTTT3MRVJEXJN4DG'}}, 'collector_id': 2388152558, 'corporation_id': None, 'counter_currency': None, 'coupon_amount': 0, 'currency_id': 'ARS', 'date_approved': '2025-04-14T17:15:12.000-04:00', 'date_created': '2025-04-14T17:15:11.000-04:00', 'date_last_updated': '2025-04-14T17:15:12.000-04:00', 'date_of_expiration': None, 'deduction_schema': None, 'description': 'PadelPals 6h14', 'differential_pricing_id': None, 'external_reference': None, 'fee_details': [{'amount': 41, 'fee_payer': 'collector', 'type': 'mercadopago_fee'}], 'financing_group': None, 'id': 108418929904, 'installments': 1, 'integrator_id': None, 'issuer_id': '2005', 'live_mode': True, 'marketplace_owner': 2388152558, 'merchant_account_id': None, 'merchant_number': None, 'metadata': {}, 'money_release_date': '2025-05-02T17:15:12.000-04:00', 'money_release_schema': None, 'money_release_status': 'pending', 'notification_url': None, 'operation_type': 'regular_payment', 'order': {'id': '30340938392', 'type': 'mercadopago'}, 'payer': {'email': 'test_user_426007166@testuser.com', 'entity_type': None, 'first_name': None, 'id': '2388139006', 'identification': {'number': '1111111', 'type': 'DNI'}, 'last_name': None, 'operator_id': None, 'phone': {'number': None, 'extension': None, 'area_code': None}, 'type': None}, 'payment_method': {'id': 'account_money', 'issuer_id': '2005', 'type': 'account_money'}, 'payment_method_id': 'account_money', 'payment_type_id': 'account_money', 'platform_id': None, 'point_of_interaction': {'business_info': {'branch': 'Merchant Services', 'sub_unit': 'checkout_pro', 'unit': 'online_payments'}, 'transaction_data': {'e2e_id': None}, 'type': 'CHECKOUT'}, 'pos_id': None, 'processing_mode': 'aggregator', 'refunds': [], 'release_info': None, 'shipping_amount': 0, 'sponsor_id': None, 'statement_descriptor': None, 'status': 'approved', 'status_detail': 'accredited', 'store_id': None, 'tags': None, 'taxes_amount': 0, 'transaction_amount': 1000, 'transaction_amount_refunded': 0, 'transaction_details': {'acquirer_reference': None, 'external_resource_url': None, 'financial_institution': None, 'installment_amount': 0, 'net_received_amount': 959, 'overpaid_amount': 0, 'payable_deferral_period': None, 'payment_method_reference_id': None, 'total_paid_amount': 1000}}}
        """

        merchant_order_id = payment["order"]["id"]
        merchant_order_response = mp_sdk.merchant_order().get(merchant_order_id)
        merchant_order = merchant_order_response["reponse"]

        logger.info(f"{merchant_order = }")

    logger.info(f"{request = }")
    logger.info(f"{request.query_params = }")
    logger.info(f"{request.headers = }")
    logger.info(f"{await request.json() = }")

    return Response(status_code=status.HTTP_200_OK)
