# Repository Collaborators
# Single source of truth: collaborators.yaml

locals {
  # Load collaborators from YAML file
  collaborators_raw = yamldecode(file("${path.module}/collaborators.yaml"))
  collaborators     = local.collaborators_raw.collaborators

  # Extract reviewers (must be collaborators with push+ permission)
  reviewers = [
    for collab in local.collaborators :
    collab.username
    if lookup(collab, "is_reviewer", false) == true
  ]

  # File patterns that require review with descriptions
  codeowner_patterns = [
    {
      description = "Default owners for everything in the repo"
      patterns    = ["*"]
    },
    {
      description = "Core package code - requires review from maintainers"
      patterns    = ["/pymlb_statsapi/"]
    },
    {
      description = "Tests - maintainers review"
      patterns    = ["/tests/"]
    },
    {
      description = "Infrastructure and CI/CD - requires admin review"
      patterns    = ["/.github/", "/scripts/"]
    },
    {
      description = "Documentation"
      patterns    = ["/docs/", "*.md"]
    },
    {
      description = "Configuration files - requires careful review"
      patterns    = ["pyproject.toml", "setup.py", "*.cfg", "*.ini"]
    },
  ]

  # Generate CODEOWNERS content
  reviewers_list = join(" ", [for r in local.reviewers : "@${r}"])

  codeowners_content = <<-EOT
    # Code Owners for PyMLB StatsAPI
    # Auto-generated from collaborators.yaml - DO NOT EDIT MANUALLY
    #
    # These users/teams will be automatically requested for review when someone
    # opens a pull request that modifies files matching the patterns below.
    #
    # More info: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners

    ${join("\n\n", [
      for group in local.codeowner_patterns :
      "# ${group.description}\n${join("\n", [for pattern in group.patterns : "${pattern} ${local.reviewers_list}"])}"
    ])}
  EOT
}

# Create collaborator resources from YAML
resource "github_repository_collaborator" "collaborators" {
  for_each = {
    for collab in local.collaborators :
    collab.username => collab
    if collab.username != "power-edge"  # Skip org owner (already has access)
  }

  repository = github_repository.repo.name
  username   = each.value.username
  permission = each.value.permission
}

# Output for use in other resources
output "collaborators_list" {
  description = "List of all collaborators"
  value       = [for collab in local.collaborators : collab.username]
}

output "reviewers_list" {
  description = "List of users who can review PRs"
  value       = local.reviewers
}
