from uuid import UUID

from sqlmodel import Field, SQLModel


class Court(SQLModel):
    court_public_id: UUID = Field()
    business_public_id: UUID = Field()
    price_per_hour: float = Field()
