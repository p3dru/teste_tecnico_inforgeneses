# Testing Guide

## Overview
This test suite provides comprehensive coverage (80%+) for the FastAPI backend using `pytest` and `pytest-asyncio`.

## Test Structure

```
tests/
├── conftest.py           # Fixtures and test infrastructure
├── test_auth.py          # Authentication endpoint tests (8 tests)
├── test_upload.py        # File upload endpoint tests (7 tests)
├── test_reports.py       # Reports endpoint tests (8 tests)
└── requirements-test.txt # Test dependencies
```

## Running Tests

### Quick Start
```bash
cd backend
./run_tests.sh
```

### Manual Execution
```bash
# Install dependencies
pip install -r tests/requirements-test.txt

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v

# Run specific test
pytest tests/test_auth.py::TestAuthentication::test_login_success -v
```

## Test Coverage

### Authentication (`test_auth.py`)
- ✅ User creation (success/duplicate)
- ✅ Login (success/wrong password/non-existent user)
- ✅ Token validation (valid/invalid/missing)
- ✅ Protected endpoint access

### Upload (`test_upload.py`)
- ✅ Image upload with mocked filesystem
- ✅ File type validation
- ✅ Authentication requirement
- ✅ GPS coordinates handling
- ✅ Kestra flow triggering
- ✅ Error handling (filesystem errors)

### Reports (`test_reports.py`)
- ✅ List reports (empty/with data)
- ✅ User isolation (users only see own reports)
- ✅ Pagination (skip/limit)
- ✅ Report detail retrieval
- ✅ Not found handling
- ✅ Unauthorized access prevention

## Key Features

### Async Testing
All tests use `pytest-asyncio` for proper async/await support.

### Database Isolation
Each test gets a fresh SQLite in-memory database via `db_session` fixture.

### Mocking Strategy
- **Kestra Client**: Mocked to avoid external API calls
- **Filesystem**: Mocked to prevent disk pollution
- **MongoDB**: Can be extended with `mongomock` if needed

### Fixtures
- `db_session`: Fresh async DB session per test
- `client`: HTTP test client with DB override
- `test_user`: Pre-created user for auth tests
- `auth_headers`: Valid JWT token headers
- `authenticated_client`: Pre-authenticated client
- `mock_kestra_trigger`: Kestra API mock

## Coverage Goals

Target: **80%+ coverage**

Current coverage includes:
- All API endpoints
- Authentication flow
- File upload logic
- Database operations
- Error handling

## CI/CD Integration

Add to your CI pipeline:
```yaml
- name: Run Tests
  run: |
    cd backend
    pip install -r tests/requirements-test.txt
    pytest tests/ --cov=app --cov-fail-under=80
```

## Troubleshooting

### Import Errors
Ensure you're running from the `backend` directory:
```bash
cd backend
pytest tests/
```

### Async Warnings
The `pytest.ini` file configures async mode. If you see warnings, verify:
```ini
asyncio_mode = auto
```

### Coverage Not Reaching 80%
Run with detailed report:
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```
