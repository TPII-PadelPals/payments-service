from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PaymentBase(SQLModel):
    match_public_id: UUID = Field()
    user_public_id: UUID = Field()
    amount: float = Field()


class PaymentCreate(PaymentBase):
    pass


class PaymentInmutable(SQLModel):
    public_id: UUID = Field(default=uuid4(), unique=True)


# class PaymentMercadoPago(SQLModel):
#     preference_id: str = Field()


class Payment(PaymentBase, PaymentInmutable, table=True):
    id: int = Field(default=None, primary_key=True)

    __tablename__ = "payments"


class PaymentPublic(PaymentBase, PaymentInmutable):
    pay_url: str = Field()
