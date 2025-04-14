from fastapi import APIRouter

from app.api.routes import items, items_service, paiements

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
api_router.include_router(paiements.router, prefix="/paiements", tags=["paiements"])
