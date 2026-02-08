
import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app


@pytest.mark.asyncio
async def test_get_activities():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data


@pytest.mark.asyncio
async def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Soccer Team"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Signup
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert response.status_code == 200
        assert f"Signed up {test_email}" in response.json()["message"]
        # Unregister
        response = await ac.post(f"/activities/{activity}/unregister", json={"email": test_email})
        assert response.status_code == 200
        assert f"Unregistered {test_email}" in response.json()["message"]


@pytest.mark.asyncio
async def test_signup_duplicate():
    test_email = "lucas@mergington.edu"  # Already in Soccer Team
    activity = "Soccer Team"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


@pytest.mark.asyncio
async def test_unregister_not_found():
    test_email = "notfound@mergington.edu"
    activity = "Soccer Team"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(f"/activities/{activity}/unregister", json={"email": test_email})
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
