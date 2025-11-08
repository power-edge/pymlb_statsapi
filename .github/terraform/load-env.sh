#!/bin/bash
# Load environment variables from .env file
# Usage: source ./load-env.sh

set -a  # automatically export all variables
source .env
set +a

echo "✓ Environment loaded from .env"
echo "  GITHUB_OWNER: $GITHUB_OWNER"
echo "  GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
echo "  AWS_PROFILE: $AWS_PROFILE"
echo "  GITHUB_TOKEN: ${GITHUB_TOKEN:+[SET]}${GITHUB_TOKEN:-[NOT SET]}"
echo ""
echo "If GITHUB_TOKEN is not set, add it to .env file:"
echo "  GITHUB_TOKEN=ghp_your_token_here"
