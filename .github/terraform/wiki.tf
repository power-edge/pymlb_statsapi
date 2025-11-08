# GitHub Wiki Infrastructure Management
#
# Note: GitHub wikis are Git repositories themselves.
# This Terraform configuration enables the wiki feature and manages
# the wiki content as repository files that get deployed via GitHub Actions.

# Enable wiki on the repository
resource "github_repository" "wiki_enabled" {
  name        = data.github_repository.repo.name
  description = "A clean, Pythonic wrapper for MLB Stats API with automatic schema-driven parameter validation"

  homepage_url = "https://pymlb-statsapi.readthedocs.io/"

  visibility = "public"

  has_issues      = true
  has_discussions = true
  has_projects    = true
  has_wiki        = true # Enable wiki

  # Enable vulnerability alerts and automated security fixes
  vulnerability_alerts   = true
  delete_branch_on_merge = true

  # Allow squash merging (recommended for feature branches)
  allow_squash_merge = true
  allow_merge_commit = true
  allow_rebase_merge = true

  # Topics/tags for discoverability
  topics = [
    "mlb",
    "baseball",
    "stats",
    "api",
    "python",
    "sports",
    "statsapi",
    "python3",
    "schema-driven",
    "mlb-stats",
    "baseball-data",
    "sports-data",
  ]

  lifecycle {
    prevent_destroy = true
  }
}

# Wiki content is managed in /wiki directory and deployed via workflow
# See .github/workflows/wiki.yml for deployment automation
