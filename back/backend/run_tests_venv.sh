#!/bin/bash
set -e

echo "🧪 Setting up test environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -r tests/requirements-test.txt

# Run tests
echo ""
echo "🚀 Running tests with coverage..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    -v

echo ""
echo "✅ Tests completed!"
echo "📊 Coverage report: htmlcov/index.html"

# Deactivate virtual environment
deactivate
