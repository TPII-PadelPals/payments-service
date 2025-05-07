from uuid import UUID

from app.core.config import settings
from app.models.business import Business
from app.models.courts import Court
from app.utilities.exceptions import NotFoundException

from .base_service import BaseService


class BusinessService(BaseService):
    def __init__(self) -> None:
        """Init the service."""
        super().__init__()
        self._set_base_url(
            settings.BUSINESS_SERVICE_HOST, settings.BUSINESS_SERVICE_PORT
        )
        if settings.BUSINESS_SERVICE_API_KEY:
            self.set_base_headers({"x-api-key": settings.BUSINESS_SERVICE_API_KEY})

    async def get_court(self, court_public_id: UUID) -> Court:
        courts = (await self.get("/api/v1/padel-courts/"))["data"]
        for court in courts:
            if court["court_public_id"] == str(court_public_id):
                return Court(**court)
        raise NotFoundException(f"Business '{court_public_id}'")

    async def get_business(self, business_public_id: UUID) -> Business:
        businesses = (await self.get("/api/v1/business/"))["data"]
        for business in businesses:
            if business["public_id"] == str(business_public_id):
                return Business(**business)
        raise NotFoundException(f"Business '{business_public_id}'")
