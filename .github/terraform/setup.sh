#!/usr/bin/env bash
# Terraform setup script for pymlb_statsapi
# Hydrates backend configuration from environment variables

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
echo -e "${BLUE}  PyMLB StatsAPI Terraform Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}Error: Terraform is not installed${NC}"
    echo "Install with: brew install terraform"
    exit 1
fi

echo -e "${GREEN}✓ Terraform found: $(terraform version | head -n1)${NC}"
echo

# Function to prompt for value with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local var_name="$3"
    local current_value="${!var_name}"

    if [ -n "$current_value" ]; then
        default="$current_value"
    fi

    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " value
        value=${value:-$default}
    else
        read -p "$prompt: " value
    fi

    eval "$var_name='$value'"
}

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${CYAN}Found existing .env file, loading configuration...${NC}"
    # shellcheck disable=SC1091
    source .env
    echo -e "${GREEN}✓ Loaded existing configuration${NC}"
    echo

    read -p "Use existing configuration? [Y/n]: " use_existing
    use_existing=${use_existing:-Y}

    if [[ $use_existing =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Using existing configuration${NC}"
    else
        echo -e "${YELLOW}Reconfiguring...${NC}"
        rm -f .env
    fi
else
    echo -e "${YELLOW}No .env file found, creating new configuration...${NC}"
fi

# If .env doesn't exist, prompt for configuration
if [ ! -f ".env" ]; then
    echo
    echo -e "${BLUE}=== Backend Type ===${NC}"
    echo "  1) S3 (power-edge-sports.terraform - default)"
    echo "  2) S3 (custom bucket)"
    echo "  3) Local (stored in git - not recommended)"
    echo
    read -p "Choice [1]: " backend_type
    backend_type=${backend_type:-1}

    case $backend_type in
        1)
            # Use default power-edge-sports bucket
            S3_BUCKET="power-edge-sports.terraform"
            S3_KEY="states/pymlb_statsapi/.github/terraform/main.tfstate"
            S3_REGION="us-east-1"
            S3_ENCRYPT="true"
            DYNAMODB_TABLE=""
            GITHUB_OWNER="power-edge"
            GITHUB_REPOSITORY="pymlb_statsapi"
            GITHUB_FULL_NAME=""
            AWS_PROFILE=""

            echo -e "${GREEN}Using default configuration:${NC}"
            echo -e "  Bucket: ${CYAN}$S3_BUCKET${NC}"
            echo -e "  Key:    ${CYAN}$S3_KEY${NC}"
            echo -e "  Region: ${CYAN}$S3_REGION${NC}"
            echo

            read -p "Customize settings? [y/N]: " customize
            if [[ $customize =~ ^[Yy]$ ]]; then
                prompt_with_default "S3 Bucket" "$S3_BUCKET" "S3_BUCKET"
                prompt_with_default "S3 Key" "$S3_KEY" "S3_KEY"
                prompt_with_default "S3 Region" "$S3_REGION" "S3_REGION"
                prompt_with_default "Enable encryption [true/false]" "$S3_ENCRYPT" "S3_ENCRYPT"
                prompt_with_default "DynamoDB table for locking (optional)" "$DYNAMODB_TABLE" "DYNAMODB_TABLE"
                prompt_with_default "AWS Profile (optional)" "$AWS_PROFILE" "AWS_PROFILE"
                prompt_with_default "GitHub Owner" "$GITHUB_OWNER" "GITHUB_OWNER"
                prompt_with_default "GitHub Repository" "$GITHUB_REPOSITORY" "GITHUB_REPOSITORY"
            fi
            ;;

        2)
            # Custom S3 bucket
            echo
            echo -e "${BLUE}=== Custom S3 Backend ===${NC}"
            prompt_with_default "S3 Bucket name" "my-terraform-state-bucket" "S3_BUCKET"
            prompt_with_default "S3 Key (path to state file)" "states/pymlb_statsapi/.github/terraform/main.tfstate" "S3_KEY"
            prompt_with_default "S3 Region" "us-east-1" "S3_REGION"
            prompt_with_default "Enable encryption [true/false]" "true" "S3_ENCRYPT"
            prompt_with_default "DynamoDB table for locking (optional)" "" "DYNAMODB_TABLE"
            prompt_with_default "AWS Profile (optional)" "" "AWS_PROFILE"
            prompt_with_default "GitHub Owner" "power-edge" "GITHUB_OWNER"
            prompt_with_default "GitHub Repository" "pymlb_statsapi" "GITHUB_REPOSITORY"
            GITHUB_FULL_NAME=""
            ;;

        3)
            # Local backend
            echo -e "${RED}Local backend not yet supported via this script${NC}"
            echo "To use local backend:"
            echo "  1. Edit main.tf and change 'backend \"s3\" {}' to 'backend \"local\" {}'"
            echo "  2. Run: terraform init -reconfigure"
            exit 1
            ;;

        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac

    # Save configuration to .env
    cat > .env <<EOF
# Terraform Backend Configuration
# Generated by setup.sh on $(date)

# S3 Backend Configuration
S3_BUCKET=$S3_BUCKET
S3_KEY=$S3_KEY
S3_REGION=$S3_REGION
S3_ENCRYPT=$S3_ENCRYPT

# Optional: DynamoDB table for state locking
DYNAMODB_TABLE=$DYNAMODB_TABLE

# GitHub Configuration
GITHUB_OWNER=$GITHUB_OWNER
GITHUB_REPOSITORY=$GITHUB_REPOSITORY
GITHUB_FULL_NAME=$GITHUB_FULL_NAME

# AWS Profile (optional)
AWS_PROFILE=$AWS_PROFILE
EOF

    echo
    echo -e "${GREEN}✓ Configuration saved to .env${NC}"
fi

# Load configuration
# shellcheck disable=SC1091
source .env

echo
echo -e "${BLUE}=== Current Configuration ===${NC}"
echo -e "  ${BLUE}Backend:${NC}"
echo -e "    S3 Bucket:      ${CYAN}$S3_BUCKET${NC}"
echo -e "    S3 Key:         ${CYAN}$S3_KEY${NC}"
echo -e "    S3 Region:      ${CYAN}$S3_REGION${NC}"
echo -e "    Encryption:     ${CYAN}$S3_ENCRYPT${NC}"
if [ -n "$DYNAMODB_TABLE" ]; then
    echo -e "    DynamoDB Table: ${CYAN}$DYNAMODB_TABLE${NC}"
fi
if [ -n "$AWS_PROFILE" ]; then
    echo -e "    AWS Profile:    ${CYAN}$AWS_PROFILE${NC}"
fi
echo -e "  ${BLUE}GitHub:${NC}"
echo -e "    Owner:          ${CYAN}$GITHUB_OWNER${NC}"
echo -e "    Repository:     ${CYAN}$GITHUB_REPOSITORY${NC}"
if [ -n "$GITHUB_FULL_NAME" ]; then
    echo -e "    Full Name:      ${CYAN}$GITHUB_FULL_NAME${NC}"
else
    echo -e "    Full Name:      ${CYAN}$GITHUB_OWNER/$GITHUB_REPOSITORY${NC}"
fi
echo

# Check AWS credentials
if [ -n "$AWS_PROFILE" ]; then
    export AWS_PROFILE="$AWS_PROFILE"
    echo -e "${CYAN}Using AWS profile: $AWS_PROFILE${NC}"
fi

if ! aws sts get-caller-identity &>/dev/null; then
    echo -e "${YELLOW}Warning: Unable to verify AWS credentials${NC}"
    echo "Make sure you have configured AWS credentials:"
    echo "  aws configure"
    if [ -n "$AWS_PROFILE" ]; then
        echo "  Or: aws configure --profile $AWS_PROFILE"
    fi
    echo
    read -p "Continue anyway? [y/N]: " continue_choice
    if [[ ! $continue_choice =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ AWS credentials verified${NC}"
    aws sts get-caller-identity
    echo
fi

# Check if S3 bucket exists
echo -e "${CYAN}Checking S3 bucket...${NC}"
if aws s3 ls "s3://$S3_BUCKET" &>/dev/null; then
    echo -e "${GREEN}✓ S3 bucket exists and is accessible${NC}"
else
    echo -e "${YELLOW}Warning: Cannot access S3 bucket: $S3_BUCKET${NC}"
    read -p "Create bucket? [y/N]: " create_bucket
    if [[ $create_bucket =~ ^[Yy]$ ]]; then
        if [ "$S3_REGION" == "us-east-1" ]; then
            aws s3 mb "s3://$S3_BUCKET"
        else
            aws s3 mb "s3://$S3_BUCKET" --region "$S3_REGION"
        fi
        echo -e "${GREEN}✓ Created S3 bucket${NC}"
    else
        echo -e "${YELLOW}Continuing without bucket verification...${NC}"
    fi
fi
echo

# Generate backend configuration file
echo -e "${CYAN}Generating backend configuration...${NC}"

# Create backend.tf from template
if [ -f "backend.tf.template" ]; then
    # Use template
    envsubst < backend.tf.template > backend.tf
else
    # Generate directly
    cat > backend.tf <<EOF
# Backend configuration for PyMLB StatsAPI
# Generated by setup.sh on $(date)
# DO NOT COMMIT THIS FILE - it's in .gitignore

terraform {
  backend "s3" {
    bucket         = "$S3_BUCKET"
    key            = "$S3_KEY"
    region         = "$S3_REGION"
    encrypt        = $S3_ENCRYPT
EOF

    if [ -n "$DYNAMODB_TABLE" ]; then
        echo "    dynamodb_table = \"$DYNAMODB_TABLE\"" >> backend.tf
    fi

    if [ -n "$AWS_PROFILE" ]; then
        echo "    profile        = \"$AWS_PROFILE\"" >> backend.tf
    fi

    echo "  }" >> backend.tf
    echo "}" >> backend.tf
fi

echo -e "${GREEN}✓ Generated backend.tf${NC}"
echo

# Generate backend.hcl for alternative init method
cat > backend.hcl <<EOF
# Backend configuration for terraform init
# Generated by setup.sh on $(date)

bucket = "$S3_BUCKET"
key    = "$S3_KEY"
region = "$S3_REGION"
encrypt = $S3_ENCRYPT
EOF

if [ -n "$DYNAMODB_TABLE" ]; then
    echo "dynamodb_table = \"$DYNAMODB_TABLE\"" >> backend.hcl
fi

if [ -n "$AWS_PROFILE" ]; then
    echo "profile = \"$AWS_PROFILE\"" >> backend.hcl
fi

echo -e "${GREEN}✓ Generated backend.hcl${NC}"
echo

# Check for GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}Warning: GITHUB_TOKEN environment variable is not set${NC}"
    echo "You'll need this to apply changes. Set it with:"
    echo "  export GITHUB_TOKEN='ghp_your_token_here'"
    echo
    read -p "Continue? [y/N]: " continue_choice
    if [[ ! $continue_choice =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ GITHUB_TOKEN is set${NC}"
    echo
fi

# Initialize Terraform
echo -e "${BLUE}=== Initializing Terraform ===${NC}"
echo

read -p "Initialize Terraform now? [Y/n]: " init_now
init_now=${init_now:-Y}

if [[ $init_now =~ ^[Yy]$ ]]; then
    # Check if already initialized
    if [ -d ".terraform" ]; then
        echo -e "${YELLOW}Terraform already initialized${NC}"
        read -p "Reinitialize (reconfigure backend)? [y/N]: " reinit
        if [[ $reinit =~ ^[Yy]$ ]]; then
            terraform init -reconfigure
        else
            terraform init -upgrade
        fi
    else
        terraform init
    fi

    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Setup Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo "Next steps:"
    echo "  1. Review changes:  ${CYAN}terraform plan${NC}"
    echo "  2. Apply changes:   ${CYAN}terraform apply${NC}"
    echo
    echo "Configuration saved in:"
    echo "  ${CYAN}.env${NC}        - Your settings (not committed)"
    echo "  ${CYAN}backend.tf${NC}   - Generated backend config (not committed)"
    echo "  ${CYAN}backend.hcl${NC}  - Alternative init method (not committed)"
    echo
else
    echo
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Configuration Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo
    echo "To initialize Terraform, run:"
    echo "  ${CYAN}terraform init${NC}"
    echo
    echo "Or reinitialize if needed:"
    echo "  ${CYAN}terraform init -reconfigure${NC}"
    echo
fi

echo "For help, see: ${CYAN}README.md${NC}"
