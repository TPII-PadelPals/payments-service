from uuid import UUID

from sqlmodel import Field, SQLModel


class PaymentBase(SQLModel):
    match_public_id: UUID = Field()
    match_title: str = Field()
    user_telegram_id: int = Field()
    amount: float = Field()


class PaymentCreate(PaymentBase):
    pass


class PaymentPublic(PaymentBase):
    url: str = Field()
