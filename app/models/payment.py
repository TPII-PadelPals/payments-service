from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, UniqueConstraint


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
    __table_args__ = (
        UniqueConstraint(
            "match_public_id",
            "user_public_id",
            name="uq_user_match_constraint",
        ),
    )


class PaymentURL(SQLModel):
    pay_url: str = Field()


class PaymentExtended(Payment, PaymentURL):
    pass


class PaymentExtendedPublic(PaymentBase, PaymentInmutable, PaymentMutable, PaymentURL):
    pass
