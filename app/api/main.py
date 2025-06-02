from fastapi import APIRouter, Depends

from app.api.routes import items, items_service, notifications, payments
from app.utilities.dependencies import get_token_header

ROOT_ROUTE = "/payments"

api_router_with_api_key = APIRouter(
    dependencies=[Depends(get_token_header)],
)
api_router_with_api_key.include_router(items.router, prefix="/items", tags=["items"])
api_router_with_api_key.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)

api_router_with_api_key.include_router(
    payments.router, prefix=f"{ROOT_ROUTE}", tags=["payments"]
)


api_router_without_api_key = APIRouter()
api_router_without_api_key.include_router(
    notifications.router, prefix=f"{ROOT_ROUTE}/notifications", tags=["notifications"]
)
