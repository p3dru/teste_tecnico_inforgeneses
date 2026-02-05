#!/bin/bash
set -e

echo "🔧 Ensuring shared volume permissions for API..."

# Fix permissions if needed (non-blocking)
if [ -d "/shared-data" ]; then
    chmod -R 777 /shared-data 2>/dev/null || echo "⚠️  Could not modify all permissions (non-critical)"
fi

echo "✅ API startup checks complete"

# Execute the original command
exec "$@"
