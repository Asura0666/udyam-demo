# tests/test_udyam_routes.py
import json
import uuid
from unittest.mock import AsyncMock
from fastapi import status

BASE_URL = "/api/v1/udyam"


def test_list_udyam_route(test_client):
    routes = [route.path for route in test_client.app.routes]
    assert f"{BASE_URL}/{{app_id}}/submit" in routes


def test_submit_final_form_success(test_client, monkeypatch, final_form_payload):
    app_id = str(uuid.uuid4())
    mock_response = {
        "registrationId": "REG123",
        "status": "submitted"
    }

    mock_service = AsyncMock()
    mock_service.submit_registration.return_value = mock_response

    monkeypatch.setattr("src.routes.udyam_routes.UdyamService", lambda: mock_service)
    monkeypatch.setattr("src.routes.udyam_routes.get_session", lambda: AsyncMock())

    response = test_client.post(
        f"{BASE_URL}/{app_id}/submit",
        content=json.dumps(final_form_payload)
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response


def test_submit_final_form_not_found(test_client, monkeypatch, final_form_payload):
    app_id = str(uuid.uuid4())

    mock_service = AsyncMock()
    mock_service.submit_registration.side_effect = ValueError("Application not found")

    monkeypatch.setattr("src.routes.udyam_routes.UdyamService", lambda: mock_service)
    monkeypatch.setattr("src.routes.udyam_routes.get_session", lambda: AsyncMock())

    response = test_client.post(
        f"{BASE_URL}/{app_id}/submit",
        content=json.dumps(final_form_payload)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Application not found"}
