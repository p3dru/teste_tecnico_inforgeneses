#!/bin/bash
set -e

echo "🧪 Running Test Suite with Coverage..."

# Install test dependencies if needed
pip install -q -r tests/requirements-test.txt

# Run pytest with coverage
pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-fail-under=80 \
    -v

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report generated in htmlcov/index.html"
