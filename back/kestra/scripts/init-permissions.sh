#!/bin/bash
set -e

echo "🔧 Checking shared volume permissions..."

# Try to fix permissions, but don't fail if we can't
mkdir -p /shared-data/uploads /shared-data/models 2>/dev/null || true
chmod -R 777 /shared-data 2>/dev/null || echo "⚠️  Running as non-root, skipping chmod (permissions should be pre-configured)"

echo "✅ Starting Kestra..."

# Execute the original Kestra entrypoint
exec docker-entrypoint.sh "$@"
