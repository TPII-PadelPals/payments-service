from uuid import UUID

from sqlmodel import Field, SQLModel


class PaymentPublic(SQLModel):
    match_public_id: UUID = Field()
    user_public_id: UUID = Field()
    title: str = Field()
    amount: float = Field()
    pay_url: str = Field()
