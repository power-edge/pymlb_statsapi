# Maintainers & Code Owners

This document explains how to manage maintainers and code owners for the PyMLB StatsAPI project.

## Current Setup

The project uses **CODEOWNERS** file managed via Terraform to automatically request reviews from maintainers when PRs are opened.

### Branch Protection Settings

- **Require code owner reviews**: ✅ Enabled
- **Required approving reviews**: 1
- **Dismiss stale reviews**: ✅ Enabled
- **Require conversation resolution**: ✅ Enabled

This means:
1. PRs must be reviewed by at least one code owner (from CODEOWNERS file)
2. Reviews become stale when new commits are pushed
3. All conversations must be resolved before merging

## Adding Maintainers

### Option 1: Individual Users (Current Setup)

To add individual maintainers, update the Terraform configuration:

1. **Edit `.github/terraform/variables.tf`**:
   ```hcl
   variable "codeowners" {
     type        = list(string)
     description = "List of GitHub usernames who are code owners/maintainers"
     default     = ["nikolauspschuetz", "newmaintainer", "anothermaintainer"]
   }
   ```

2. **Update CODEOWNERS content in `.github/terraform/main.tf`**:
   ```hcl
   content = <<-EOT
     # Default owners for everything
     * @nikolauspschuetz @newmaintainer @anothermaintainer

     # Core package code
     /pymlb_statsapi/ @nikolauspschuetz @newmaintainer

     # etc...
   EOT
   ```

3. **Apply changes**:
   ```bash
   cd .github/terraform
   terraform apply
   ```

### Option 2: GitHub Teams (Recommended for Organizations)

For organizations, you can create teams and use them in CODEOWNERS.

#### Step 1: Create a GitHub Team

**Via GitHub UI:**
1. Go to your organization: https://github.com/orgs/power-edge/teams
2. Click "New team"
3. Team name: `pymlb-maintainers`
4. Description: "Core maintainers for PyMLB StatsAPI"
5. Visibility: "Visible" (or "Secret" if needed)
6. Add members

**Via Terraform:**

Add to `.github/terraform/main.tf`:

```hcl
# Create maintainers team
resource "github_team" "maintainers" {
  name        = "pymlb-maintainers"
  description = "Core maintainers for PyMLB StatsAPI"
  privacy     = "closed"  # or "secret"
}

# Add team members
resource "github_team_membership" "nikolaus" {
  team_id  = github_team.maintainers.id
  username = "nikolauspschuetz"
  role     = "maintainer"
}

resource "github_team_membership" "maintainer2" {
  team_id  = github_team.maintainers.id
  username = "another-maintainer"
  role     = "member"
}

# Grant team access to repository
resource "github_team_repository" "maintainers" {
  team_id    = github_team.maintainers.id
  repository = data.github_repository.repo.name
  permission = "maintain"  # or "admin", "push", "pull"
}
```

#### Step 2: Update CODEOWNERS to Use Team

```hcl
resource "github_repository_file" "codeowners" {
  # ...
  content = <<-EOT
    # Default owners (using team)
    * @power-edge/pymlb-maintainers

    # Core package code
    /pymlb_statsapi/ @power-edge/pymlb-maintainers

    # Infrastructure requires admin
    /.github/ @nikolauspschuetz

    # etc...
  EOT
}
```

#### Step 3: Apply Changes

```bash
cd .github/terraform
terraform apply
```

## CODEOWNERS Patterns

Common patterns you can use in CODEOWNERS:

```plaintext
# Everything
* @owner

# Specific directory
/path/to/dir/ @owner

# Specific files
*.js @js-owner
*.py @python-owner

# Nested paths
/docs/**/*.md @docs-team

# Multiple owners (ANY can approve)
* @owner1 @owner2 @owner3

# Teams
* @org/team-name
```

## Requiring Multiple Approvals

To require approvals from multiple people:

1. **Update Terraform** (`.github/terraform/main.tf`):
   ```hcl
   required_pull_request_reviews {
     dismiss_stale_reviews           = true
     require_code_owner_reviews      = true
     required_approving_review_count = 2  # Changed from 1
     restrict_dismissals             = false
   }
   ```

2. **Apply changes**:
   ```bash
   cd .github/terraform
   terraform apply
   ```

This will require 2 approvals from code owners before a PR can be merged.

## Advanced: Different Owners for Different Parts

You can require different people to review different parts of the codebase:

```hcl
content = <<-EOT
  # Default owner
  * @nikolauspschuetz

  # Python code requires Python experts
  /pymlb_statsapi/*.py @nikolauspschuetz @python-expert

  # Tests can be reviewed by test team
  /tests/ @nikolauspschuetz @test-team

  # Infrastructure requires admin approval
  /.github/ @nikolauspschuetz
  /scripts/ @nikolauspschuetz

  # Documentation can be reviewed by docs team
  /docs/ @docs-team @nikolauspschuetz
  *.md @docs-team

  # Critical config files need admin
  pyproject.toml @nikolauspschuetz
  /.github/terraform/ @nikolauspschuetz
EOT
```

## Team Roles & Permissions

GitHub Teams support different roles:

- **Maintainer**: Can manage team membership and settings
- **Member**: Regular team member

Repository permissions:

- **admin**: Full access, can delete repo
- **maintain**: Manage repo without destructive actions
- **push**: Read, write, and push
- **triage**: Read and manage issues/PRs
- **pull**: Read-only access

Example with different permissions:

```hcl
resource "github_team_repository" "maintainers" {
  team_id    = github_team.maintainers.id
  repository = data.github_repository.repo.name
  permission = "maintain"
}

resource "github_team_repository" "contributors" {
  team_id    = github_team.contributors.id
  repository = data.github_repository.repo.name
  permission = "push"
}
```

## Testing CODEOWNERS

After setting up CODEOWNERS:

1. Create a test branch
2. Make a small change
3. Open a PR
4. Check that the correct reviewers are auto-assigned

## Troubleshooting

### CODEOWNERS not working

1. **Check file location**: Must be `.github/CODEOWNERS`, `CODEOWNERS`, or `docs/CODEOWNERS`
2. **Check syntax**: Use `@username` for users, `@org/team` for teams
3. **Verify permissions**: Code owners must have write access to the repo
4. **Check branch protection**: `require_code_owner_reviews` must be true

### Team not found

- Ensure the team exists in your organization
- Use correct format: `@org-name/team-name`
- Team must have access to the repository

### Reviews not required

- Check branch protection settings in Terraform
- Verify `require_code_owner_reviews = true`
- Apply Terraform changes: `terraform apply`

## Current Configuration

As of this documentation:

- **Code owners**: @nikolauspschuetz
- **Required reviews**: 1 from code owners
- **Managed via**: Terraform IaC
- **File location**: `.github/CODEOWNERS` (auto-created by Terraform)

## Resources

- [GitHub CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [GitHub Teams Documentation](https://docs.github.com/en/organizations/organizing-members-into-teams/about-teams)
- [Terraform GitHub Provider - Teams](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/team)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
