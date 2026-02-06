import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestAuthentication:
    """Test suite for authentication endpoints."""
    
    async def test_create_user_success(self, client: AsyncClient):
        """Test successful user creation."""
        response = await client.post(
            "/auth/users",
            json={"username": "newuser", "password": "newpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "hashed_password" not in data  # Should not expose password
    
    async def test_create_user_duplicate(self, client: AsyncClient, test_user):
        """Test creating a user with existing username fails."""
        response = await client.post(
            "/auth/users",
            json={"username": test_user.username, "password": "anypass"}
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login returns access token."""
        response = await client.post(
            "/auth/token",
            data={"username": "testuser", "password": "testpass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password fails."""
        response = await client.post(
            "/auth/token",
            data={"username": "testuser", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user fails."""
        response = await client.post(
            "/auth/token",
            data={"username": "ghost", "password": "anypass"}
        )
        assert response.status_code == 401
    
    async def test_protected_endpoint_without_token(self, client: AsyncClient):
        """Test accessing protected endpoint without token fails."""
        response = await client.get("/reports")
        assert response.status_code == 401
    
    async def test_protected_endpoint_with_invalid_token(self, client: AsyncClient):
        """Test accessing protected endpoint with invalid token fails."""
        response = await client.get(
            "/reports",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        assert response.status_code == 401
    
    async def test_protected_endpoint_with_valid_token(self, authenticated_client: AsyncClient):
        """Test accessing protected endpoint with valid token succeeds."""
        response = await authenticated_client.get("/reports")
        assert response.status_code == 200
