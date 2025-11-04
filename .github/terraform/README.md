# GitHub Repository Terraform Configuration

This directory contains Terraform configuration for managing GitHub repository settings, branch protection rules, and other repository resources as Infrastructure as Code (IaC).

## Prerequisites

1. **Install Terraform**: Version >= 1.5.0
   ```bash
   brew install terraform  # macOS
   # or download from https://www.terraform.io/downloads
   ```

2. **GitHub Personal Access Token**:
   - Go to GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
   - Generate new token with scopes:
     - `repo` (Full control of private repositories)
     - `admin:repo_hook` (Full control of repository hooks)
     - `delete_repo` (Delete repositories)
   - Export the token:
     ```bash
     export GITHUB_TOKEN="ghp_your_token_here"
     ```

3. **AWS Credentials** (if using S3 backend):
   - Configure AWS credentials via `~/.aws/credentials` or environment variables
   - Ensure you have access to the S3 bucket

## Backend Configuration

This Terraform configuration uses a **variable-driven backend** setup. The backend configuration is generated from your settings during setup.

### Quick Setup (Recommended)

```bash
# Navigate to terraform directory
cd .github/terraform

# Run interactive setup
./setup.sh
```

The setup script will:
1. Prompt for backend configuration (S3 bucket, region, etc.)
2. Save your settings to `.env` (gitignored)
3. Generate `backend.tf` with your configuration
4. Initialize Terraform automatically

### Backend Options

#### Option 1: Default Power-Edge Bucket (Team Default)

Uses: `s3://power-edge-sports.terraform/states/pymlb_statsapi/.github/terraform/main.tfstate`

```bash
./setup.sh
# Choose option 1, accept defaults
```

#### Option 2: Custom S3 Bucket (Bring Your Own)

Use your own S3 bucket for state storage:

```bash
./setup.sh
# Choose option 2, enter your bucket details
```

Required information:
- S3 bucket name
- S3 region
- State file path/key
- (Optional) DynamoDB table for state locking
- (Optional) AWS profile

#### Option 3: Manual Configuration

If you prefer manual setup:

```bash
# Copy template
cp .env.template .env

# Edit .env with your settings
vim .env

# Run setup
./setup.sh
```

### Configuration File Structure

After running `setup.sh`, you'll have:

- `.env` - Your backend settings (gitignored, not committed)
- `backend.tf` - Generated Terraform backend config (gitignored)
- `backend.hcl` - Alternative config format (gitignored)

These files are **not committed** to version control, allowing each user/environment to bring their own backend configuration.

## Quick Start

```bash
# Navigate to terraform directory
cd .github/terraform

# Run setup (interactive, configures backend)
./setup.sh

# After setup completes, review and apply changes
terraform plan
terraform apply
```

## What This Manages

### Branch Protection
- **Main branch**: Protected with required PR reviews and CI checks
  - Requires 1 approving review
  - Requires all CI checks to pass:
    - Unit tests on Ubuntu/macOS with Python 3.11, 3.12, 3.13
    - Build verification
    - Documentation build
  - Prevents force pushes and deletions
  - Requires conversations to be resolved before merging

### Repository Settings
- Description and homepage URL
- Topics/tags for discoverability
- Issue/discussion/project features
- Vulnerability alerts enabled
- Auto-delete merged branches
- Merge strategy options

### Issue Labels
Standard labels for issue/PR organization:
- `bug`, `enhancement`, `documentation`
- `good first issue`, `help wanted`
- `question`, `tests`, `ci/cd`
- `wontfix`, `duplicate`

## Configuration

### Customizing Branch Protection

Edit `main.tf` to modify required status checks:

```hcl
required_status_checks {
  strict = true
  contexts = [
    "test (ubuntu-latest, 3.11)",
    # Add or remove checks as needed
  ]
}
```

### Adding Secrets or Variables

If you need to manage GitHub Actions secrets:

```hcl
resource "github_actions_secret" "example" {
  repository      = data.github_repository.repo.name
  secret_name     = "MY_SECRET"
  plaintext_value = var.my_secret_value
}
```

Then add the variable to `variables.tf`:

```hcl
variable "my_secret_value" {
  type        = string
  sensitive   = true
  description = "My secret value"
}
```

## State Management

### Current Setup: S3 Backend

State is stored in S3 at:
```
s3://power-edge-sports.terraform/states/pymlb_statsapi/.github/terraform/main.tfstate
```

### Switching Backends

#### From S3 to Local

1. Edit `main.tf`, change `backend "s3" {}` to `backend "local" {}`
2. Run:
   ```bash
   terraform init -backend-config=backend-local.hcl -migrate-state
   ```

#### From Local to S3

1. Edit `main.tf`, change `backend "local" {}` to `backend "s3" {}`
2. Run:
   ```bash
   terraform init -backend-config=backend-s3.hcl -migrate-state
   ```

### S3 State Bucket Structure

```
s3://power-edge-sports.terraform/
└── states/
    ├── pymlb_statsapi/
    │   └── .github/
    │       └── terraform/
    │           └── main.tfstate
    └── other-project/
        └── ...
```

## Common Operations

### View Current State
```bash
terraform show
```

### List Resources
```bash
terraform state list
```

### Import Existing Resources
If resources already exist in GitHub:
```bash
terraform import github_branch_protection.main "pymlb_statsapi:main"
```

### Destroy Resources (Use with caution!)
```bash
terraform destroy
```

## Troubleshooting

### Authentication Issues
```bash
# Verify token is set
echo $GITHUB_TOKEN

# Test token with GitHub API
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### State Lock Issues
```bash
# If state is locked, force unlock (use carefully)
terraform force-unlock <lock-id>
```

### Drift Detection
```bash
# Check if actual state differs from Terraform state
terraform plan -refresh-only
```

## Best Practices

1. **Always run `terraform plan`** before `apply` to review changes
2. **Use version control** for all Terraform files (already done via git)
3. **Never commit** `terraform.tfstate` or `.tfvars` files with secrets
4. **Review changes carefully** when modifying branch protection
5. **Test in a fork first** if making major changes

## CI/CD Integration (Future Enhancement)

Consider adding a GitHub Actions workflow to automatically apply Terraform changes:

```yaml
name: Terraform

on:
  push:
    paths:
      - '.github/terraform/**'
    branches: [main]
  pull_request:
    paths:
      - '.github/terraform/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform plan
      - run: terraform apply -auto-approve
        if: github.ref == 'refs/heads/main'
```

## Resources

- [Terraform GitHub Provider Documentation](https://registry.terraform.io/providers/integrations/github/latest/docs)
- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)
