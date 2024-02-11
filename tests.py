import httpx
import pytest

# BASE_URL = "http://localhost:8000"
BASE_URL = "http://host.docker.internal:8000"


@pytest.fixture
def client():
    return httpx.Client(base_url=BASE_URL)


def test_create_user(client):
    """Test user creation endpoint."""
    response = client.post("/api/v1/users", json={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert "verified" in response.json() and response.json()["verified"] is False


def test_create_user_duplicate(client):
    """Test creating a user that already exists."""
    response = client.post("/api/v1/users", json={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_without_verification(client):
    """Test logging in without verification."""
    response = client.post("/api/v1/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "User not verified. Please verify your email."


def test_verify_user(client):
    """Test verifying a user."""
    response = client.post("/api/v1/verify-user", json={
        "email": "testuser@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User testuser@example.com has been verified"


def test_login_after_verification(client):
    """Test logging in after verification."""
    response = client.post("/api/v1/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
