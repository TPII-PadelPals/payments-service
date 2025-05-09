from typing import Any


class MercadoPagoService:
    def __init__(self, mp_sdk: Any) -> None:
        self.mp_sdk = mp_sdk

    def get_merchant_order(self, merchant_order_id: int) -> Any:
        return self.mp_sdk.merchant_order().get(merchant_order_id)

    def get_payment(self, payment_id: int) -> Any:
        return self.mp_sdk.payment().get(payment_id)
