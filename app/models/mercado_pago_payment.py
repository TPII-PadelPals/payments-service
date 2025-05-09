from uuid import UUID

from sqlmodel import Field, SQLModel


class MercadoPagoPaymentBase(SQLModel):
    public_id: UUID = Field(foreign_key="payments.public_id", ondelete="CASCADE")
    preference_id: str = Field()


class MercadoPagoPaymentCreate(MercadoPagoPaymentBase):
    pass


class MercadoPagoPayment(MercadoPagoPaymentBase, table=True):
    id: int = Field(default=None, primary_key=True)

    __tablename__ = "mercadopago-payments"


class MercadoPagoPaymentExtended(MercadoPagoPayment):
    pay_url: str = Field()


class MercadoPagoPaymentPublic(MercadoPagoPaymentBase):
    pass
