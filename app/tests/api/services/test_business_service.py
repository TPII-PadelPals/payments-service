import uuid
from typing import Any

from app.services.business_service import (
    BusinessService,
)


async def test_get_court(monkeypatch: Any) -> None:
    n_courts = 3
    expected_courts = []
    for i in range(n_courts):
        expected_courts.append(
            {
                "court_public_id": str(uuid.uuid4()),
                "business_public_id": str(uuid.uuid4()),
                "name": f"Court {i}",
                "price_per_hour": 1000.0 + i,
            }
        )

    async def mock_get(self: Any, url: str) -> Any:  # noqa: ARG001
        assert url == "/api/v1/padel-courts/"
        return {"data": expected_courts, "count": len(expected_courts)}

    monkeypatch.setattr(BusinessService, "get", mock_get)
    for expected_court in expected_courts:
        result_court = await BusinessService().get_court(
            expected_court["court_public_id"]  # type: ignore
        )
        assert str(result_court.court_public_id) == expected_court["court_public_id"]
        assert (
            str(result_court.business_public_id) == expected_court["business_public_id"]
        )
        assert result_court.price_per_hour == expected_court["price_per_hour"]
