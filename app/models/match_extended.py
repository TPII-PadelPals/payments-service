import datetime
from enum import Enum
from uuid import UUID

from sqlmodel import Field, SQLModel


class ReserveStatus(str, Enum):
    INSIDE = "inside"
    REJECTED = "Rejected"
    OUTSIDE = "outside"


class Match(SQLModel):
    public_id: UUID = Field()
    court_public_id: UUID = Field()
    date: datetime.date = Field()
    time: int = Field()


class MatchPlayer(SQLModel):
    user_public_id: UUID = Field()
    match_public_id: UUID = Field()


class MatchExtended(Match):
    match_players: list[MatchPlayer]
