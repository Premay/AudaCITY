from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_auth_service, get_catalog_service
from app.main import app


@pytest.fixture
def client() -> TestClient:
    service = AsyncMock()
    service.register.return_value = {"user": {"id": "student-1"}}
    service.login.return_value = {"access_token": "token"}
    service.get_user.return_value = {"id": "student-1"}
    service.get_profile.return_value = {"id": "student-1", "email": "student@example.com"}
    catalog = AsyncMock()
    catalog.fetch.return_value = [{"id": "exam-1", "code": "JAMB", "name": "JAMB"}]
    app.dependency_overrides[get_auth_service] = lambda: service
    app.dependency_overrides[get_catalog_service] = lambda: catalog
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_register_uses_backend_auth_service(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "Student@Example.com",
            "password": "secure-password",
            "full_name": "Ada Student",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"user": {"id": "student-1"}}


def test_profile_requires_bearer_token(client: TestClient) -> None:
    response = client.get("/api/v1/profile")

    assert response.status_code == 401


def test_profile_is_loaded_for_authenticated_user(client: TestClient) -> None:
    response = client.get(
        "/api/v1/profile", headers={"Authorization": "Bearer student-token"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == "student-1"


def test_exams_are_loaded_for_authenticated_user(client: TestClient) -> None:
    response = client.get("/api/v1/exams", headers={"Authorization": "Bearer student-token"})

    assert response.status_code == 200
    assert response.json()[0]["code"] == "JAMB"
