# Collaborators Management

## Single Source of Truth: `collaborators.yaml`

All repository access, code review requirements, and CODEOWNERS are driven from `collaborators.yaml`.

### Structure

```yaml
collaborators:
  - username: power-edge
    permission: admin      # admin, maintain, push, triage, pull
    is_reviewer: true      # Can review PRs
    is_owner: true         # Organization owner

  - username: nikolauspschuetz
    permission: push       # write access
    is_reviewer: true      # Can review PRs
    is_admin: true         # Can bypass some protections
```

### What Gets Generated

1. **GitHub Collaborators** (`collaborators.tf`)
   - Creates `github_repository_collaborator` resources
   - Skips `power-edge` (org owner already has access)
   - Grants permissions as specified

2. **CODEOWNERS File** (`main.tf`)
   - Auto-generated from `codeowner_patterns` in `collaborators.tf`
   - All reviewers (`is_reviewer: true`) are added to all patterns
   - Committed to `.github/CODEOWNERS`

3. **Review Requirements**
   - Branch protection uses CODEOWNERS
   - All reviewers must have at least `push` permission

### How to Add a New Collaborator

1. Edit `collaborators.yaml`:
   ```yaml
   - username: new-user
     permission: push
     is_reviewer: false  # or true if they can review PRs
   ```

2. Apply Terraform:
   ```bash
   cd .github/terraform
   source load-env.sh
   terraform apply
   ```

3. User must accept invitation via email/GitHub

### File Patterns Requiring Review

Defined in `collaborators.tf` → `codeowner_patterns`:
- `*` - Everything (default)
- `/pymlb_statsapi/` - Core package
- `/tests/` - Test files
- `/.github/` - CI/CD and infrastructure
- `/scripts/` - Scripts
- `/docs/` - Documentation
- `*.md` - Markdown files
- `pyproject.toml`, `setup.py`, `*.cfg`, `*.ini` - Config files

To modify patterns, edit the `codeowner_patterns` list in `collaborators.tf`.

### Validation

- Reviewers must have at least `push` permission (enforced in code)
- All patterns get all reviewers (simplified management)
- CODEOWNERS is auto-committed on Terraform apply

### Outputs

- `collaborators_list` - All collaborator usernames
- `reviewers_list` - Usernames who can review PRs
