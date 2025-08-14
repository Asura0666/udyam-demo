# tests/test_pan_routes.py
import json
from unittest.mock import AsyncMock
from fastapi import status

BASE_URL = "/api/v1/pan"


def test_list_pan_route(test_client):
    routes = [route.path for route in test_client.app.routes]
    assert f"{BASE_URL}/verify" in routes


def test_verify_pan_success(test_client, monkeypatch, pan_payload):
    mock_response = {
        "verified": True,
        "appId": str(pan_payload["appId"])
    }

    mock_service = AsyncMock()
    mock_service.verify_pan.return_value = mock_response

    monkeypatch.setattr("src.routes.pan_routes.PanService", lambda: mock_service)
    monkeypatch.setattr("src.routes.pan_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify", content=json.dumps(pan_payload))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response


def test_verify_pan_not_found(test_client, monkeypatch, pan_payload):
    mock_service = AsyncMock()
    mock_service.verify_pan.side_effect = ValueError("PAN not found")

    monkeypatch.setattr("src.routes.pan_routes.PanService", lambda: mock_service)
    monkeypatch.setattr("src.routes.pan_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify", content=json.dumps(pan_payload))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "PAN not found"}


def test_verify_pan_internal_error(test_client, monkeypatch, pan_payload):
    mock_service = AsyncMock()
    mock_service.verify_pan.side_effect = Exception("Service down")

    monkeypatch.setattr("src.routes.pan_routes.PanService", lambda: mock_service)
    monkeypatch.setattr("src.routes.pan_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify", content=json.dumps(pan_payload))

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Internal Server Error"}
