#!/usr/bin/env bash
# Hydrates GitHub repository secrets for pymlb_statsapi
# Requires: gh CLI, GITHUB_TOKEN environment variable

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GitHub Secrets Hydration${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Load environment configuration
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Run ./setup.sh first to configure environment"
    exit 1
fi

# shellcheck disable=SC1091
source .env

REPO="${GITHUB_OWNER}/${GITHUB_REPOSITORY}"

echo -e "${CYAN}Repository: ${REPO}${NC}"
echo

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install with: brew install gh"
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI found: $(gh --version | head -n1)${NC}"

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN environment variable is not set${NC}"
    echo "Set it with: export GITHUB_TOKEN='ghp_your_token_here'"
    exit 1
fi

export GH_TOKEN="$GITHUB_TOKEN"

echo -e "${GREEN}✓ GitHub token configured${NC}"
echo

# Check if repository exists
if ! gh repo view "$REPO" &>/dev/null; then
    echo -e "${RED}Error: Repository $REPO does not exist${NC}"
    echo "Create repository first via Terraform"
    exit 1
fi

echo -e "${GREEN}✓ Repository $REPO exists${NC}"
echo

# Function to set secret
set_secret() {
    local secret_name="$1"
    local secret_value="$2"
    local env_name="${3:-}"

    if [ -n "$env_name" ]; then
        echo -e "${CYAN}Setting secret ${secret_name} in environment ${env_name}...${NC}"
        echo "$secret_value" | gh secret set "$secret_name" --repo "$REPO" --env "$env_name"
    else
        echo -e "${CYAN}Setting repository secret ${secret_name}...${NC}"
        echo "$secret_value" | gh secret set "$secret_name" --repo "$REPO"
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Successfully set ${secret_name}${NC}"
    else
        echo -e "${RED}✗ Failed to set ${secret_name}${NC}"
        return 1
    fi
}

# Function to create environment if it doesn't exist
create_environment() {
    local env_name="$1"

    echo -e "${CYAN}Checking if environment ${env_name} exists...${NC}"

    # GitHub CLI doesn't have direct environment creation, but setting a secret creates it
    # We'll check by trying to list secrets for the environment
    if gh api "repos/${REPO}/environments/${env_name}" &>/dev/null; then
        echo -e "${GREEN}✓ Environment ${env_name} already exists${NC}"
    else
        echo -e "${YELLOW}Environment ${env_name} does not exist, will be created when first secret is set${NC}"
    fi
}

echo -e "${BLUE}=== PyPI Secrets ===${NC}"
echo

# Check if secrets are already in .env (extended)
if [ -f ".env" ] && grep -q "PYPI_TOKEN" .env 2>/dev/null; then
    # shellcheck disable=SC1091
    source .env
fi

# Prompt for PYPI_TOKEN if not set
if [ -z "$PYPI_TOKEN" ]; then
    echo -e "${YELLOW}PyPI Token not found in environment${NC}"
    echo "Get your PyPI token from: https://pypi.org/manage/account/token/"
    echo
    read -sp "Enter PYPI_TOKEN (or press Enter to skip): " PYPI_TOKEN
    echo

    if [ -z "$PYPI_TOKEN" ]; then
        echo -e "${YELLOW}Skipping PYPI_TOKEN${NC}"
    else
        # Save to .env for future use
        if ! grep -q "PYPI_TOKEN" .env; then
            echo >> .env
            echo "# PyPI Publishing Token" >> .env
            echo "# Get from: https://pypi.org/manage/account/token/" >> .env
            echo "PYPI_TOKEN=$PYPI_TOKEN" >> .env
            echo -e "${GREEN}✓ Saved PYPI_TOKEN to .env${NC}"
        fi
    fi
fi

# Prompt for TEST_PYPI_TOKEN if not set
if [ -z "$TEST_PYPI_TOKEN" ]; then
    echo -e "${YELLOW}Test PyPI Token not found in environment${NC}"
    echo "Get your Test PyPI token from: https://test.pypi.org/manage/account/token/"
    echo
    read -sp "Enter TEST_PYPI_TOKEN (or press Enter to skip): " TEST_PYPI_TOKEN
    echo

    if [ -z "$TEST_PYPI_TOKEN" ]; then
        echo -e "${YELLOW}Skipping TEST_PYPI_TOKEN${NC}"
    else
        # Save to .env for future use
        if ! grep -q "TEST_PYPI_TOKEN" .env; then
            echo >> .env
            echo "# Test PyPI Publishing Token" >> .env
            echo "# Get from: https://test.pypi.org/manage/account/token/" >> .env
            echo "TEST_PYPI_TOKEN=$TEST_PYPI_TOKEN" >> .env
            echo -e "${GREEN}✓ Saved TEST_PYPI_TOKEN to .env${NC}"
        fi
    fi
fi

echo

# Create environments
create_environment "pypi"
create_environment "testpypi"

echo

# Set secrets
if [ -n "$PYPI_TOKEN" ]; then
    set_secret "PYPI_TOKEN" "$PYPI_TOKEN" "pypi"
else
    echo -e "${YELLOW}⚠ Skipping PYPI_TOKEN (not provided)${NC}"
fi

if [ -n "$TEST_PYPI_TOKEN" ]; then
    set_secret "TEST_PYPI_TOKEN" "$TEST_PYPI_TOKEN" "testpypi"
else
    echo -e "${YELLOW}⚠ Skipping TEST_PYPI_TOKEN (not provided)${NC}"
fi

echo
echo -e "${BLUE}=== Additional Repository Secrets ===${NC}"
echo

# Add any other secrets needed
# Example: CODECOV_TOKEN, etc.

echo -e "${YELLOW}No additional secrets configured${NC}"
echo

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Secrets Hydration Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo

echo "You can verify secrets with:"
echo -e "  ${CYAN}gh secret list --repo $REPO${NC}"
echo -e "  ${CYAN}gh api repos/$REPO/environments/pypi/secrets${NC}"
echo
