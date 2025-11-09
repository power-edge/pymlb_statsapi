# Quick Start Guide

Get up and running with Terraform for GitHub repository management in 5 minutes.

## For Team Members (Power-Edge)

If you're part of the power-edge team and want to use the shared S3 bucket:

```bash
# 1. Navigate to terraform directory
cd .github/terraform

# 2. Run setup
./setup.sh

# 3. Choose option 1 (default power-edge bucket)
#    Press Enter to accept all defaults

# 4. Verify configuration
terraform plan

# 5. Apply changes
terraform apply
```

**That's it!** Your backend is configured to use:
- Bucket: `power-edge-sports.terraform`
- Key: `states/pymlb_statsapi/.github/terraform/main.tfstate`

## For Contributors (Bring Your Own Bucket)

If you want to use your own S3 bucket for testing:

```bash
# 1. Navigate to terraform directory
cd .github/terraform

# 2. Run setup
./setup.sh

# 3. Choose option 2 (custom S3 bucket)

# 4. Enter your details:
#    - S3 bucket name: your-terraform-bucket
#    - Region: us-east-1 (or your preferred region)
#    - Key: states/pymlb_statsapi/.github/terraform/main.tfstate
#    - Encryption: true
#    - DynamoDB table: (optional, leave empty for now)
#    - AWS Profile: (optional, or leave empty for default)

# 5. Review and apply
terraform plan
terraform apply
```

## Prerequisites Checklist

Before running setup, make sure you have:

- [ ] Terraform installed (`brew install terraform`)
- [ ] AWS credentials configured (`aws configure`)
- [ ] GitHub token set (`export GITHUB_TOKEN='ghp_...'`)
- [ ] S3 bucket created (or will be created by script)

## What Happens During Setup?

The `setup.sh` script will:

1. ✅ Check if Terraform is installed
2. ✅ Prompt for backend configuration
3. ✅ Save your settings to `.env`
4. ✅ Verify AWS credentials
5. ✅ Check if S3 bucket exists (offer to create if not)
6. ✅ Generate `backend.tf` with your configuration
7. ✅ Initialize Terraform
8. ✅ You're ready to go!

## Files Created (Not Committed)

After setup, these files exist locally but are **not committed** to git:

- `.env` - Your backend configuration variables
- `backend.tf` - Generated Terraform backend block
- `backend.hcl` - Alternative backend config format
- `.terraform/` - Terraform working directory
- `.terraform.lock.hcl` - Provider lock file

## Common Commands

```bash
# View what would change
terraform plan

# Apply changes
terraform apply

# View current state
terraform show

# List all resources
terraform state list

# Format code
terraform fmt

# Validate configuration
terraform validate

# Destroy all resources (careful!)
terraform destroy
```

## Reconfiguring Backend

If you need to change your backend settings:

```bash
# Edit your settings
vim .env

# Rerun setup
./setup.sh

# Migrate state (if switching buckets)
terraform init -migrate-state
```

## Switching Between Buckets

If you want to switch from team bucket to personal or vice versa:

```bash
# Remove current configuration
rm .env backend.tf

# Rerun setup with new settings
./setup.sh
```

## Troubleshooting

### "Cannot access S3 bucket"

```bash
# Verify AWS credentials
aws sts get-caller-identity

# List buckets
aws s3 ls

# Create bucket if needed
aws s3 mb s3://your-bucket-name
```

### "GITHUB_TOKEN not set"

```bash
# Set token
export GITHUB_TOKEN='ghp_your_token_here'

# Or add to ~/.bashrc or ~/.zshrc
echo "export GITHUB_TOKEN='ghp_your_token_here'" >> ~/.bashrc
```

### "Backend initialization failed"

```bash
# Remove Terraform cache
rm -rf .terraform

# Rerun setup
./setup.sh
```

## Getting Help

- Read the full [README.md](README.md)
- Check [Terraform GitHub Provider Docs](https://registry.terraform.io/providers/integrations/github/latest/docs)
- Open an issue in the repository

## Next Steps

After successfully running Terraform:

1. Review the [main.tf](main.tf) to understand what's being managed
2. Explore [variables.tf](variables.tf) for customization options
3. Check out the GitHub repository settings to see the applied changes
4. Make changes to [main.tf](main.tf) and apply incrementally

Happy Infrastructure as Code! 🚀
