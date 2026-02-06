import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sql import Report, ReportStatus, User


@pytest.mark.asyncio
class TestReports:
    """Test suite for reports retrieval endpoints."""
    
    async def test_list_reports_empty(
        self,
        authenticated_client: AsyncClient
    ):
        """Test listing reports when user has none."""
        response = await authenticated_client.get("/reports")
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    async def test_list_reports_with_data(
        self,
        authenticated_client: AsyncClient,
        test_user: User,
        db_session: AsyncSession
    ):
        """Test listing reports returns user's reports."""
        # Create test reports
        report1 = Report(
            id="test-id-1",
            user_id=test_user.id,
            file_path="test1.png",
            status=ReportStatus.DONE.value
        )
        report2 = Report(
            id="test-id-2",
            user_id=test_user.id,
            file_path="test2.png",
            status=ReportStatus.PROCESSING.value
        )
        db_session.add_all([report1, report2])
        await db_session.commit()
        
        response = await authenticated_client.get("/reports")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] in ["test-id-1", "test-id-2"]
    
    async def test_list_reports_user_isolation(
        self,
        authenticated_client: AsyncClient,
        test_user: User,
        db_session: AsyncSession
    ):
        """Test that users only see their own reports."""
        # Create another user
        other_user = User(
            username="otheruser",
            hashed_password="hash"
        )
        db_session.add(other_user)
        await db_session.commit()
        await db_session.refresh(other_user)
        
        # Create reports for both users
        my_report = Report(
            id="my-report",
            user_id=test_user.id,
            file_path="mine.png",
            status=ReportStatus.DONE.value
        )
        their_report = Report(
            id="their-report",
            user_id=other_user.id,
            file_path="theirs.png",
            status=ReportStatus.DONE.value
        )
        db_session.add_all([my_report, their_report])
        await db_session.commit()
        
        response = await authenticated_client.get("/reports")
        assert response.status_code == 200
        data = response.json()
        
        # Should only see own report
        assert len(data) == 1
        assert data[0]["id"] == "my-report"
    
    async def test_list_reports_pagination(
        self,
        authenticated_client: AsyncClient,
        test_user: User,
        db_session: AsyncSession
    ):
        """Test pagination parameters work correctly."""
        # Create 15 reports
        reports = [
            Report(
                id=f"report-{i}",
                user_id=test_user.id,
                file_path=f"test{i}.png",
                status=ReportStatus.DONE.value
            )
            for i in range(15)
        ]
        db_session.add_all(reports)
        await db_session.commit()
        
        # Test limit
        response = await authenticated_client.get("/reports?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Test skip
        response = await authenticated_client.get("/reports?skip=10&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5  # Only 5 remaining after skipping 10
    
    async def test_get_report_detail_success(
        self,
        authenticated_client: AsyncClient,
        test_user: User,
        db_session: AsyncSession
    ):
        """Test retrieving a specific report by ID."""
        from unittest.mock import patch, AsyncMock
        
        # Mock MongoDB query to return None (no inference log found)
        with patch("app.api.endpoints.reports.InferenceLog.find_one", new_callable=AsyncMock) as mock_find:
            mock_find.return_value = None
            
            report = Report(
                id="detail-test",
                user_id=test_user.id,
                file_path="detail.png",
                status=ReportStatus.DONE.value
            )
            db_session.add(report)
            await db_session.commit()
            
            response = await authenticated_client.get("/reports/detail-test")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "detail-test"
            assert data["file_path"] == "detail.png"
    
    async def test_get_report_detail_not_found(
        self,
        authenticated_client: AsyncClient
    ):
        """Test retrieving non-existent report returns 404."""
        response = await authenticated_client.get("/reports/nonexistent-id")
        assert response.status_code == 404
    
    async def test_get_report_detail_unauthorized_access(
        self,
        authenticated_client: AsyncClient,
        test_user: User,
        db_session: AsyncSession
    ):
        """Test accessing another user's report is forbidden."""
        # Create another user
        other_user = User(
            username="otheruser",
            hashed_password="hash"
        )
        db_session.add(other_user)
        await db_session.commit()
        await db_session.refresh(other_user)
        
        # Create report for other user
        their_report = Report(
            id="their-report",
            user_id=other_user.id,
            file_path="theirs.png",
            status=ReportStatus.DONE.value
        )
        db_session.add(their_report)
        await db_session.commit()
        
        # Try to access it
        response = await authenticated_client.get("/reports/their-report")
        assert response.status_code == 404  # Should not reveal existence
