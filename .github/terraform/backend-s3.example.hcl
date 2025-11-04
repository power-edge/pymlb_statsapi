# Example S3 backend configuration
# Copy this to backend-s3.hcl and customize for your setup
#
# Usage:
#   cp backend-s3.example.hcl backend-s3.hcl
#   # Edit backend-s3.hcl with your settings
#   terraform init -backend-config=backend-s3.hcl

bucket = "your-terraform-state-bucket"
key    = "states/your-project/.github/terraform/main.tfstate"
region = "us-east-1"

# Optional: Enable state locking with DynamoDB
# dynamodb_table = "terraform-state-lock"

# Optional: Enable encryption (recommended)
encrypt = true

# Optional: Use a specific AWS profile
# profile = "your-aws-profile"
