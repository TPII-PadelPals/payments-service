from uuid import UUID

from app.core.config import settings
from app.models.match_extended import MatchExtended, MatchPlayer, ReserveStatus
from app.utilities.exceptions import NotFoundException

from .base_service import BaseService


class MatchesService(BaseService):
    def __init__(self) -> None:
        """Init the service."""
        super().__init__()
        self._set_base_url(
            settings.MATCHES_SERVICE_HTTP,
            settings.MATCHES_SERVICE_HOST,
            settings.MATCHES_SERVICE_PORT,
        )
        if settings.MATCHES_SERVICE_API_KEY:
            self.set_base_headers({"x-api-key": settings.MATCHES_SERVICE_API_KEY})

    async def get_player_match(
        self, user_public_id: UUID, match_public_id: UUID
    ) -> MatchExtended:
        matches_extended = (
            await self.get(f"/api/v1/players/{user_public_id}/matches/")
        )["data"]
        for match_extended in matches_extended:
            if match_extended["public_id"] == str(match_public_id):
                return MatchExtended(**match_extended)
        raise NotFoundException(f"Match '{match_public_id}'")

    async def update_match_player(
        self, user_public_id: UUID, match_public_id: UUID, status: ReserveStatus
    ) -> MatchPlayer:
        payload = {"reserve": status}
        match_player = await self.patch(
            f"/api/v1/matches/{match_public_id}/players/{user_public_id}/", json=payload
        )
        return MatchPlayer(**match_player)
