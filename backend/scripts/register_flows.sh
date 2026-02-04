#!/bin/bash

# Configuration
KESTRA_URL="http://localhost:8080/api/v1/flows"
USER="admin@kestra.io"
PASS="Admin1234"
FLOWS_DIR="../../kestra/flows"

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Registering Kestra Flows..."

# Ensure directory exists
cd "$(dirname "$0")" || exit
if [ ! -d "$FLOWS_DIR" ]; then
    echo -e "${RED}Directory not found: $FLOWS_DIR${NC}"
    exit 1
fi

# Iterate and Register
for file in "$FLOWS_DIR"/*.yaml; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo -n "Registering $filename... "
        
        response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$KESTRA_URL" \
            -u "$USER:$PASS" \
            -H "Content-Type: application/x-yaml" \
            --data-binary @"$file")
            
        if [ "$response" == "200" ]; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${RED}FAILED ($response)${NC}"
        fi
    fi
done

echo "Done."
