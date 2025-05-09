from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"


class PaymentBase(SQLModel):
    match_public_id: UUID = Field()
    user_public_id: UUID = Field()
    amount: float = Field()


class PaymentMutable(SQLModel):
    status: PaymentStatus | None = Field(default=PaymentStatus.PENDING)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentMutable):
    pass


class PaymentInmutable(SQLModel):
    public_id: UUID = Field(default=uuid4(), unique=True)


class Payment(PaymentBase, PaymentInmutable, PaymentMutable, table=True):
    id: int = Field(default=None, primary_key=True)

    __tablename__ = "payments"


class PaymentPublic(PaymentBase, PaymentInmutable, PaymentMutable):
    pay_url: str = Field()
