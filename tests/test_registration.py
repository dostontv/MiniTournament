from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_tournament():
    tournament_data = {
        "name": f"World Cup {datetime.now()}",
        "max_players": 6,
        "start_at": datetime.strptime("2025-10-01T15:00:00Z", "%Y-%m-%dT%H:%M:%SZ").isoformat(),
    }
    response = client.post("/tournaments/", json=tournament_data)
    print("Create tournament response:", response.json())
    assert response.status_code == 201
