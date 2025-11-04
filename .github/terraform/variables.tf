variable "github_owner" {
  type        = string
  description = "GitHub organization or user account name"
  default     = "power-edge"
}

variable "github_repository" {
  type        = string
  description = "GitHub repository name (without owner)"
  default     = "pymlb_statsapi"
}

variable "github_full_name" {
  type        = string
  description = "GitHub repository full name (owner/repo)"
  default     = ""
}

variable "github_token" {
  type        = string
  sensitive   = true
  description = "GitHub Personal Access Token for Terraform"
  default     = ""
}
