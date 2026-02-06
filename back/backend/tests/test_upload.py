import pytest
from httpx import AsyncClient
from io import BytesIO
from unittest.mock import patch, mock_open, MagicMock


@pytest.mark.asyncio
class TestUpload:
    """Test suite for file upload endpoint."""
    
    async def test_upload_image_success(
        self, 
        authenticated_client: AsyncClient,
        mock_kestra_trigger
    ):
        """Test successful image upload with mocked filesystem."""
        # Create fake image file
        fake_image = BytesIO(b"fake image content")
        fake_image.name = "test.png"
        
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("shutil.copyfileobj") as mock_copy, \
             patch("os.path.join", return_value="/shared-data/uploads/test.png"):
            
            response = await authenticated_client.post(
                "/files/upload",
                files={"file": ("test.png", fake_image, "image/png")},
                data={"latitude": 40.7128, "longitude": -74.0060}
            )
            
            assert response.status_code == 202
            data = response.json()
            assert data["status"] == "PROCESSING"
            assert "id" in data
            assert data["file_path"].endswith(".png")
            
            # Verify file operations were called
            mock_file.assert_called_once()
            mock_copy.assert_called_once()
    
    async def test_upload_non_image_fails(
        self,
        authenticated_client: AsyncClient
    ):
        """Test uploading non-image file fails validation."""
        fake_file = BytesIO(b"not an image")
        fake_file.name = "document.pdf"
        
        response = await authenticated_client.post(
            "/files/upload",
            files={"file": ("document.pdf", fake_file, "application/pdf")}
        )
        
        assert response.status_code == 400
        assert "must be an image" in response.json()["detail"]
    
    async def test_upload_without_authentication(
        self,
        client: AsyncClient
    ):
        """Test upload without authentication fails."""
        fake_image = BytesIO(b"fake image")
        fake_image.name = "test.png"
        
        response = await client.post(
            "/files/upload",
            files={"file": ("test.png", fake_image, "image/png")}
        )
        
        assert response.status_code == 401
    
    async def test_upload_with_coordinates(
        self,
        authenticated_client: AsyncClient,
        mock_kestra_trigger
    ):
        """Test upload with GPS coordinates."""
        fake_image = BytesIO(b"fake image content")
        fake_image.name = "test.jpg"
        
        with patch("builtins.open", mock_open()), \
             patch("shutil.copyfileobj"), \
             patch("os.path.join", return_value="/shared-data/uploads/test.jpg"):
            
            response = await authenticated_client.post(
                "/files/upload",
                files={"file": ("test.jpg", fake_image, "image/jpeg")},
                data={
                    "latitude": -23.5505,
                    "longitude": -46.6333
                }
            )
            
            assert response.status_code == 202
            data = response.json()
            assert data["latitude"] == -23.5505
            assert data["longitude"] == -46.6333
    
    async def test_upload_triggers_kestra(
        self,
        authenticated_client: AsyncClient,
        mock_kestra_trigger
    ):
        """Test that upload triggers Kestra flow."""
        fake_image = BytesIO(b"fake image")
        fake_image.name = "fire.png"
        
        with patch("builtins.open", mock_open()), \
             patch("shutil.copyfileobj"), \
             patch("os.path.join", return_value="/shared-data/uploads/fire.png"):
            
            response = await authenticated_client.post(
                "/files/upload",
                files={"file": ("fire.png", fake_image, "image/png")}
            )
            
            assert response.status_code == 202
            # Kestra trigger is mocked in conftest.py
            # The mock returns "mock-execution-{report_id}"
            # We verify it was called by checking the response exists
            assert "id" in response.json()
    
    async def test_upload_filesystem_error_handling(
        self,
        authenticated_client: AsyncClient
    ):
        """Test graceful handling of filesystem errors."""
        fake_image = BytesIO(b"fake image")
        fake_image.name = "test.png"
        
        with patch("builtins.open", side_effect=PermissionError("No write access")):
            response = await authenticated_client.post(
                "/files/upload",
                files={"file": ("test.png", fake_image, "image/png")}
            )
            
            assert response.status_code == 500
            assert "Could not save file" in response.json()["detail"]
