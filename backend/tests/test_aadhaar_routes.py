# import pytest
# from unittest.mock import AsyncMock
# from src.routes.aadhaar_routes import get_aadhaar_service

# BASE_PATH = "/api/v1/aadhaar"


# def override_service(mock_service):
#     """Helper to override aadhaar service dependency."""
#     return lambda: mock_service


# @pytest.mark.asyncio
# async def test_send_otp_success(test_client):
#     mock_response = {
#         "app_id": "app123",
#         "transaction_id": "txn456",
#         "message": "OTP sent successfully",
#     }
#     mock_service = AsyncMock()
#     mock_service.send_otp.return_value = mock_response
#     test_client.app.dependency_overrides[get_aadhaar_service] = override_service(mock_service)

#     payload = {
#         "aadhaarNumber": "123412341234",
#         "entrepreneurName": "John Doe",
#         "consent": True,
#     }
#     response = test_client.post(f"{BASE_PATH}/send-otp", json=payload)

#     assert response.status_code == 200
#     assert response.json() == mock_response
#     mock_service.send_otp.assert_awaited_once_with(
#         aadhaar_number="123412341234",
#         entrepreneur_name="John Doe",
#         consent=True,
#         session=pytest.ANY,
#     )

#     test_client.app.dependency_overrides.clear()


# @pytest.mark.asyncio
# async def test_send_otp_failure(test_client):
#     mock_service = AsyncMock()
#     mock_service.send_otp.side_effect = Exception("Something went wrong")
#     test_client.app.dependency_overrides[get_aadhaar_service] = override_service(mock_service)

#     payload = {
#         "aadhaarNumber": "123412341234",
#         "entrepreneurName": "John Doe",
#         "consent": True,
#     }
#     response = test_client.post(f"{BASE_PATH}/send-otp", json=payload)

#     assert response.status_code == 400
#     assert response.json()["detail"] == "Something went wrong"

#     test_client.app.dependency_overrides.clear()


# @pytest.mark.asyncio
# async def test_verify_otp_success(test_client):
#     mock_response = {
#         "verified": True,
#         "message": "OTP verified successfully",
#     }
#     mock_service = AsyncMock()
#     mock_service.verify_otp.return_value = mock_response
#     test_client.app.dependency_overrides[get_aadhaar_service] = override_service(mock_service)

#     payload = {
#         "app_id": "app123",
#         "transaction_id": "txn456",
#         "otp": "123456",
#     }
#     response = test_client.post(f"{BASE_PATH}/verify-otp", json=payload)

#     assert response.status_code == 200
#     assert response.json() == mock_response
#     mock_service.verify_otp.assert_awaited_once_with(
#         app_id="app123",
#         transaction_id="txn456",
#         otp="123456",
#         session=pytest.ANY,
#     )

#     test_client.app.dependency_overrides.clear()


# @pytest.mark.asyncio
# async def test_verify_otp_not_found(test_client):
#     mock_service = AsyncMock()
#     mock_service.verify_otp.side_effect = ValueError("Invalid OTP")
#     test_client.app.dependency_overrides[get_aadhaar_service] = override_service(mock_service)

#     payload = {
#         "app_id": "app123",
#         "transaction_id": "txn456",
#         "otp": "000000",
#     }
#     response = test_client.post(f"{BASE_PATH}/verify-otp", json=payload)

#     assert response.status_code == 404
#     assert response.json()["detail"] == "Invalid OTP"

#     test_client.app.dependency_overrides.clear()


# @pytest.mark.asyncio
# async def test_verify_otp_generic_error(test_client):
#     mock_service = AsyncMock()
#     mock_service.verify_otp.side_effect = Exception("Service down")
#     test_client.app.dependency_overrides[get_aadhaar_service] = override_service(mock_service)

#     payload = {
#         "app_id": "app123",
#         "transaction_id": "txn456",
#         "otp": "123456",
#     }
#     response = test_client.post(f"{BASE_PATH}/verify-otp", json=payload)

#     assert response.status_code == 400
#     assert response.json()["detail"] == "Service down"

#     test_client.app.dependency_overrides.clear()

# ----------------------------------------------------------------------------------------

# # tests/test_aadhaar_routes.py
# import pytest
# from unittest.mock import AsyncMock


# @pytest.fixture
# def fake_session():
#     """Fake DB session for dependency injection."""
#     return AsyncMock()


# @pytest.mark.asyncio
# async def test_list_routes(test_client):
#     routes = [route.path for route in test_client.app.routes]
#     print("Registered routes:", routes)
#     assert "/api/v1/aadhaar/send-otp" in routes
#     assert "/api/v1/aadhaar/verify-otp" in routes


# @pytest.mark.asyncio
# async def test_send_otp_success(test_client, monkeypatch, fake_session):
#     mock_response = {
#         "transactionId": "txn456",
#         "otpSentTo": "xxxxxx1234",
#         "appId": "app123",
#     }

#     mock_service = AsyncMock()
#     mock_service.send_otp.return_value = mock_response

#     monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
#     monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: fake_session)

#     payload = {
#         "aadhaarNumber": "123412341234",
#         "entrepreneurName": "John Doe",
#         "consent": True,
#     }

#     response = await test_client.post("/api/v1/aadhaar/send-otp", json=payload)

#     assert response.status_code == 200
#     assert response.json() == mock_response
#     mock_service.send_otp.assert_awaited_once_with(
#         aadhaar_number="123412341234",
#         entrepreneur_name="John Doe",
#         consent=True,
#         session=fake_session,
#     )


# @pytest.mark.asyncio
# async def test_send_otp_failure(test_client, monkeypatch, fake_session):
#     mock_service = AsyncMock()
#     mock_service.send_otp.side_effect = Exception("Something went wrong")

#     monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
#     monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: fake_session)

#     payload = {
#         "aadhaarNumber": "123412341234",
#         "entrepreneurName": "John Doe",
#         "consent": True,
#     }

#     response = await test_client.post("/api/v1/aadhaar/send-otp", json=payload)

#     assert response.status_code == 400
#     assert response.json() == {"detail": "Something went wrong"}


# @pytest.mark.asyncio
# async def test_verify_otp_success(test_client, monkeypatch, fake_session):
#     mock_response = {
#         "verified": True,
#         "appId": "app123"
#     }

#     mock_service = AsyncMock()
#     mock_service.verify_otp.return_value = mock_response

#     monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
#     monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: fake_session)

#     payload = {"app_id": "app123", "transaction_id": "txn456", "otp": "123456"}

#     response = await test_client.post("/api/v1/aadhaar/verify-otp", json=payload)

#     assert response.status_code == 200
#     assert response.json() == mock_response
#     mock_service.verify_otp.assert_awaited_once_with(
#         app_id="app123",
#         transaction_id="txn456",
#         otp="123456",
#         session=fake_session,
#     )


# @pytest.mark.asyncio
# async def test_verify_otp_not_found(test_client, monkeypatch, fake_session):
#     mock_service = AsyncMock()
#     mock_service.verify_otp.side_effect = ValueError("Invalid OTP")

#     monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
#     monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: fake_session)

#     payload = {"app_id": "app123", "transaction_id": "txn456", "otp": "000000"}

#     response = await test_client.post("/api/v1/aadhaar/verify-otp", json=payload)

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Invalid OTP"}


# @pytest.mark.asyncio
# async def test_verify_otp_generic_error(test_client, monkeypatch, fake_session):
#     mock_service = AsyncMock()
#     mock_service.verify_otp.side_effect = Exception("Service down")

#     monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
#     monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: fake_session)

#     payload = {"app_id": "app123", "transaction_id": "txn456", "otp": "123456"}

#     response = await test_client.post("/api/v1/aadhaar/verify-otp", json=payload)

#     assert response.status_code == 400
#     assert response.json() == {"detail": "Service down"}


# -------------------------------------------------------------------------

# tests/test_aadhaar_routes.py
import json
from unittest.mock import AsyncMock
from fastapi import status

BASE_URL = "/api/v1/aadhaar"


def test_list_routes(test_client):
    routes = [route.path for route in test_client.app.routes]
    assert f"{BASE_URL}/send-otp" in routes
    assert f"{BASE_URL}/verify-otp" in routes


def test_send_otp_success(test_client, monkeypatch, aadhaar_payload):
    mock_response = {
        "transactionId": "txn456",
        "otpSentTo": "xxxxxx1234",
        "appId": "app123",
    }

    mock_service = AsyncMock()
    mock_service.send_otp.return_value = mock_response

    monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
    monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/send-otp", content=json.dumps(aadhaar_payload))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response


def test_send_otp_failure(test_client, monkeypatch, aadhaar_payload):
    mock_service = AsyncMock()
    mock_service.send_otp.side_effect = Exception("Something went wrong")

    monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
    monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/send-otp", content=json.dumps(aadhaar_payload))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Something went wrong"}


def test_verify_otp_success(test_client, monkeypatch, otp_verify_payload):
    mock_response = {
        "verified": True,
        "appId": "app123"
    }

    mock_service = AsyncMock()
    mock_service.verify_otp.return_value = mock_response

    monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
    monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify-otp", content=json.dumps(otp_verify_payload))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response


def test_verify_otp_not_found(test_client, monkeypatch, otp_verify_payload):
    mock_service = AsyncMock()
    mock_service.verify_otp.side_effect = ValueError("Invalid OTP")

    monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
    monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify-otp", content=json.dumps(otp_verify_payload))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Invalid OTP"}


def test_verify_otp_generic_error(test_client, monkeypatch, otp_verify_payload):
    mock_service = AsyncMock()
    mock_service.verify_otp.side_effect = Exception("Service down")

    monkeypatch.setattr("src.routes.aadhaar_routes.aadhaar_service", mock_service)
    monkeypatch.setattr("src.routes.aadhaar_routes.get_session", lambda: AsyncMock())

    response = test_client.post(f"{BASE_URL}/verify-otp", content=json.dumps(otp_verify_payload))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Service down"}
