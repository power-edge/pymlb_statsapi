# Using Terraform in CI/CD

This guide shows how to use the Terraform configuration in GitHub Actions or other CI/CD systems.

## GitHub Actions Integration

### Option 1: Using Environment Variables

The simplest way to use this in GitHub Actions is via environment variables:

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

    # Set default working directory
    defaults:
      run:
        working-directory: .github/terraform

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Create backend configuration
        run: |
          cat > backend.tf <<EOF
          terraform {
            backend "s3" {
              bucket = "power-edge-sports.terraform"
              key    = "states/pymlb_statsapi/.github/terraform/main.tfstate"
              region = "us-east-1"
              encrypt = true
            }
          }
          EOF

      - name: Terraform Init
        run: terraform init

      - name: Terraform Format Check
        run: terraform fmt -check

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
          TF_VAR_github_owner: ${{ github.repository_owner }}
          TF_VAR_github_repository: ${{ github.event.repository.name }}
        run: terraform plan -out=tfplan

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
          TF_VAR_github_owner: ${{ github.repository_owner }}
          TF_VAR_github_repository: ${{ github.event.repository.name }}
        run: terraform apply -auto-approve tfplan
```

### Option 2: Using tfvars File

Create a tfvars file in the workflow:

```yaml
      - name: Create tfvars file
        run: |
          cat > terraform.tfvars <<EOF
          github_owner      = "${{ github.repository_owner }}"
          github_repository = "${{ github.event.repository.name }}"
          EOF

      - name: Terraform Plan
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
        run: terraform plan -var-file=terraform.tfvars
```

### Option 3: Using Matrix Strategy for Multiple Repos

Manage multiple repositories with a matrix:

```yaml
jobs:
  terraform:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo:
          - owner: power-edge
            name: pymlb_statsapi
          - owner: power-edge
            name: another-repo

    steps:
      # ... setup steps ...

      - name: Terraform Plan
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
          TF_VAR_github_owner: ${{ matrix.repo.owner }}
          TF_VAR_github_repository: ${{ matrix.repo.name }}
        run: terraform plan
```

## Required Secrets

Add these secrets to your GitHub repository:

1. **`GH_TERRAFORM_TOKEN`** - GitHub Personal Access Token
   - Scopes: `repo`, `admin:repo_hook`, `delete_repo`
   - Note: Different from `GITHUB_TOKEN` (which has limited permissions)

2. **`AWS_ACCESS_KEY_ID`** - AWS Access Key (for S3 backend)

3. **`AWS_SECRET_ACCESS_KEY`** - AWS Secret Key (for S3 backend)

## Environment Variables Reference

### Terraform Variables (TF_VAR_*)

Set these to override default values:

```bash
export TF_VAR_github_owner="power-edge"
export TF_VAR_github_repository="pymlb_statsapi"
export TF_VAR_github_full_name="power-edge/pymlb_statsapi"  # Optional
```

### GitHub Actions Context Variables

Available in workflows:

```yaml
${{ github.repository_owner }}           # e.g., "power-edge"
${{ github.event.repository.name }}      # e.g., "pymlb_statsapi"
${{ github.repository }}                 # e.g., "power-edge/pymlb_statsapi"
```

### Mapping to Terraform Variables

| GitHub Actions Variable | Terraform Variable | Example |
|------------------------|-------------------|---------|
| `github.repository_owner` | `github_owner` | `power-edge` |
| `github.event.repository.name` | `github_repository` | `pymlb_statsapi` |
| `github.repository` | `github_full_name` | `power-edge/pymlb_statsapi` |

## Example: Full CI/CD Workflow

Complete example with all features:

```yaml
name: Terraform Infrastructure

on:
  push:
    paths:
      - '.github/terraform/**'
    branches: [main]
  pull_request:
    paths:
      - '.github/terraform/**'
  workflow_dispatch:
    inputs:
      apply:
        description: 'Apply changes'
        required: false
        type: boolean
        default: false

jobs:
  terraform:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: .github/terraform

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.6.0

      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Generate backend configuration
        run: |
          cat > backend.tf <<EOF
          terraform {
            backend "s3" {
              bucket  = "power-edge-sports.terraform"
              key     = "states/${{ github.event.repository.name }}/.github/terraform/main.tfstate"
              region  = "us-east-1"
              encrypt = true
            }
          }
          EOF

      - name: Terraform Init
        run: terraform init

      - name: Terraform Format
        run: terraform fmt -check
        continue-on-error: true

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        id: plan
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
          TF_VAR_github_owner: ${{ github.repository_owner }}
          TF_VAR_github_repository: ${{ github.event.repository.name }}
        run: |
          terraform plan -out=tfplan -no-color
          echo "plan_exitcode=$?" >> $GITHUB_OUTPUT

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan 📖

            <details>
            <summary>Show Plan</summary>

            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\`

            </details>

            *Pushed by: @${{ github.actor }}, Action: \`${{ github.event_name }}\`*`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            })

      - name: Terraform Apply
        if: |
          (github.ref == 'refs/heads/main' && github.event_name == 'push') ||
          (github.event_name == 'workflow_dispatch' && github.event.inputs.apply == 'true')
        env:
          GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
          TF_VAR_github_owner: ${{ github.repository_owner }}
          TF_VAR_github_repository: ${{ github.event.repository.name }}
        run: terraform apply -auto-approve tfplan
```

## Local Testing with CI Variables

Test locally with the same variables CI will use:

```bash
export TF_VAR_github_owner="power-edge"
export TF_VAR_github_repository="pymlb_statsapi"
export GITHUB_TOKEN="ghp_your_token"

terraform plan
```

## Troubleshooting CI

### Issue: "Error initializing backend"

**Solution:** Ensure AWS credentials are configured correctly:

```yaml
- name: Debug AWS Credentials
  run: |
    aws sts get-caller-identity
    aws s3 ls s3://power-edge-sports.terraform/
```

### Issue: "Error acquiring state lock"

**Solution:** Add state locking with DynamoDB or use `-lock=false` (not recommended):

```yaml
run: terraform plan -lock=false
```

### Issue: "Error: Invalid provider configuration"

**Solution:** Ensure `GITHUB_TOKEN` is set:

```yaml
env:
  GITHUB_TOKEN: ${{ secrets.GH_TERRAFORM_TOKEN }}
```

## Best Practices

1. **Use Plan Artifacts:** Save plan and apply it (prevents drift)
   ```yaml
   terraform plan -out=tfplan
   terraform apply tfplan
   ```

2. **Validate Before Apply:** Always run validate and plan first

3. **Comment on PRs:** Show plan output in PR comments

4. **Use Workspaces:** For multiple environments
   ```bash
   terraform workspace select production
   ```

5. **Version Pin:** Lock Terraform and provider versions

6. **Secure Secrets:** Never log sensitive variables

## Advanced: Terraform Cloud Integration

For teams, consider Terraform Cloud:

```yaml
- name: Setup Terraform
  uses: hashicorp/setup-terraform@v3
  with:
    cli_config_credentials_token: ${{ secrets.TF_API_TOKEN }}

- name: Terraform Init
  run: terraform init
  # backend config in main.tf:
  # backend "remote" {
  #   organization = "power-edge-sports"
  #   workspaces {
  #     name = "pymlb-statsapi-prod"
  #   }
  # }
```

## Reference

- [GitHub Actions Context](https://docs.github.com/en/actions/learn-github-actions/contexts)
- [Terraform in CI/CD](https://developer.hashicorp.com/terraform/tutorials/automation/github-actions)
- [GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs)
