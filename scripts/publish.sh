#!/usr/bin/env bash
#
# Publish package to PyPI or TestPyPI
# Usage:
#   ./scripts/publish.sh [testpypi|pypi]
#
# Prerequisites:
#   1. Copy .env.example to .env
#   2. Fill in your PyPI tokens in .env
#   3. Run: uv sync --group dev

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load .env if it exists
if [ -f "$PROJECT_DIR/.env" ]; then
    echo -e "${GREEN}Loading environment from .env${NC}"
    set -a
    source "$PROJECT_DIR/.env"
    set +a
else
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo -e "Copy .env.example to .env and configure your tokens:"
    echo -e "  cp .env.example .env"
    echo -e "  # Edit .env with your tokens"
    exit 1
fi

# Determine target repository
TARGET="${1:-pypi}"

if [ "$TARGET" = "testpypi" ]; then
    echo -e "${GREEN}Publishing to TestPyPI...${NC}"
    export TWINE_USERNAME="${TEST_PYPI_USERNAME:-__token__}"
    export TWINE_PASSWORD="${TEST_PYPI_PASSWORD}"
    REPO_ARG="--repository testpypi"
elif [ "$TARGET" = "pypi" ]; then
    echo -e "${GREEN}Publishing to PyPI...${NC}"
    export TWINE_USERNAME="${TWINE_USERNAME:-__token__}"
    export TWINE_PASSWORD="${TWINE_PASSWORD}"
    REPO_ARG=""
else
    echo -e "${RED}Error: Invalid target '$TARGET'${NC}"
    echo "Usage: $0 [testpypi|pypi]"
    exit 1
fi

# Check if credentials are set
if [ -z "$TWINE_PASSWORD" ] || [ "$TWINE_PASSWORD" = "pypi-your-token-here" ] || [ "$TWINE_PASSWORD" = "pypi-your-test-token-here" ]; then
    echo -e "${RED}Error: PyPI token not configured in .env${NC}"
    echo "Edit .env and set your token"
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if dist/ exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo -e "${YELLOW}No dist/ found. Building package...${NC}"
    uv build
fi

# Upload to PyPI
echo -e "${GREEN}Uploading to $TARGET...${NC}"
uv run twine upload $REPO_ARG dist/*

echo -e "${GREEN}✓ Successfully published to $TARGET!${NC}"
