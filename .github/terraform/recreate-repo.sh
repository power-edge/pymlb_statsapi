#!/bin/bash
# Script to recreate repository with clean history via Terraform
set -e

echo "========================================="
echo "Repository Recreation with Terraform"
echo "========================================="
echo ""
echo "This will:"
echo "1. Delete the existing GitHub repository"
echo "2. Recreate it via Terraform (fully managed)"
echo "3. Push clean code with single commit"
echo "4. Create v1.0.0 release"
echo ""
read -p "Are you sure? Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Load environment
source load-env.sh

# Step 1: Delete existing repository
echo ""
echo "Step 1: Deleting existing repository..."
gh repo delete power-edge/pymlb_statsapi --yes || echo "Repository may already be deleted"

# Step 2: Remove Terraform state for old repo
echo ""
echo "Step 2: Removing old Terraform state..."
terraform state rm github_branch_default.default || true
terraform state rm github_branch_protection.main || true
terraform state rm github_issue_label.bug || true
terraform state rm github_issue_label.enhancement || true
terraform state rm github_issue_label.documentation || true
terraform state rm github_issue_label.good_first_issue || true
terraform state rm github_issue_label.help_wanted || true
terraform state rm github_issue_label.question || true
terraform state rm github_issue_label.wontfix || true
terraform state rm github_issue_label.duplicate || true
terraform state rm github_issue_label.tests || true
terraform state rm github_issue_label.ci_cd || true
terraform state rm github_repository_file.codeowners || true

# Step 3: Apply Terraform to create new repository
echo ""
echo "Step 3: Creating repository via Terraform..."
terraform apply

# Step 4: Hydrate repository secrets
echo ""
echo "Step 4: Hydrating repository secrets..."
./hydrate-secrets.sh

echo ""
echo "========================================="
echo "Repository created successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. cd back to repo root"
echo "2. Run: git remote set-url origin git@github.com-poweredgesports_gmail:power-edge/pymlb_statsapi.git"
echo "3. Create clean commit and push"
