#!/usr/bin/env bash
#
# Create a GitHub release from an existing tag
# Usage:
#   ./scripts/create_release.sh <tag>
#
# Example:
#   ./scripts/create_release.sh v1.1.1

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

if [ -z "$1" ]; then
    echo -e "${RED}Error: Tag version required${NC}"
    echo "Usage: $0 <tag>"
    echo "Example: $0 v1.1.1"
    exit 1
fi

TAG="$1"

# Check if tag exists
if ! git rev-parse "$TAG" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag '$TAG' does not exist${NC}"
    echo "Available tags:"
    git tag -l | tail -5
    exit 1
fi

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: gh CLI not found${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if already authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Get tag message
TAG_MESSAGE=$(git tag -l --format='%(contents)' "$TAG")

echo -e "${GREEN}Creating GitHub release for $TAG${NC}"
echo ""
echo "Release notes:"
echo "---"
echo "$TAG_MESSAGE"
echo "---"
echo ""

# Checkout the tag
git checkout "$TAG" 2>/dev/null || true

# Build package
echo -e "${GREEN}Building package...${NC}"
rm -rf dist/
uv build

# Create release
echo -e "${GREEN}Creating GitHub release...${NC}"
gh release create "$TAG" \
  --title "Release $TAG" \
  --notes "$TAG_MESSAGE" \
  dist/*

echo -e "${GREEN}✓ Successfully created release $TAG!${NC}"
echo "View at: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/releases/tag/$TAG"

# Return to previous branch
git checkout -
