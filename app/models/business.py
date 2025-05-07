from uuid import UUID

from sqlmodel import Field, SQLModel


class Business(SQLModel):
    business_public_id: UUID = Field()
    name: str = Field()
