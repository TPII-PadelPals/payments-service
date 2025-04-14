from uuid import UUID

from sqlmodel import Field, SQLModel


class PaiementBase(SQLModel):
    match_public_id: UUID = Field()
    match_title: str = Field()
    user_telegram_id: int = Field()
    amount: float = Field()


class PaiementCreate(PaiementBase):
    pass


class PaiementPublic(PaiementBase):
    url: str = Field()
