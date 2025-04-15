import uuid

from httpx import AsyncClient

from app.core.config import settings

# Aceptar => Generar URL de Pago => Recibir Notificación => Actualizar estado de reserva
# Rechazar (tras ser asignado) => Nada
# Rechazar (tras haver aceptado) => Solicitar reembolso
# ó
# Solicitar reembolso desde MP => Recibir notificación => Actualizar estado de reserva

# Generar URL de Pago
# -> Endpoint para generar un pago a nuestra billetera
# Notificaciones
# -> Loguear por consola o mockear endpoint

mp_sdk = settings.MERCADO_PAGO_SDK


async def test_create_match_payment(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    payload = {
        "match_public_id": str(uuid.uuid4()),
        "match_title": "PadelPals Match: PadelFIUBA 14/04/2025 10 hs",
        "user_telegram_id": 1000,
        "amount": 5000,
    }
    response = await async_client.post(
        f"{settings.API_V1_STR}/payments/",
        headers=x_api_key_header,
        json=payload,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["url"] is not None
    content.pop("url")
    assert content == payload
