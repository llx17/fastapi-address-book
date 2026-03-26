import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_login_success(client):
    """Test successful login with demo credentials."""
    response = client.post(
        "/auth/login",
        json={"username": "demo", "password": "demo123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


def test_login_invalid_username(client):
    """Test login with invalid username."""
    response = client.post(
        "/auth/login",
        json={"username": "invalid", "password": "demo123"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_login_invalid_password(client):
    """Test login with invalid password."""
    response = client.post(
        "/auth/login",
        json={"username": "demo", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_access_protected_endpoint_with_token(client):
    """Test accessing protected endpoint with valid token."""
    # Get token
    login_response = client.post(
        "/auth/login",
        json={"username": "demo", "password": "demo123"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected endpoint with token
    response = client.get(
        "/addresses/nearby",
        params={
            "latitude": 10.0,
            "longitude": 76.0,
            "distance_km": 10
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200


def test_access_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token."""
    response = client.get(
        "/addresses/nearby",
        params={
            "latitude": 10.0,
            "longitude": 76.0,
            "distance_km": 10
        }
    )
    
    assert response.status_code == 403


def test_access_protected_endpoint_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/addresses/nearby",
        params={
            "latitude": 10.0,
            "longitude": 76.0,
            "distance_km": 10
        },
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    assert response.status_code == 401
