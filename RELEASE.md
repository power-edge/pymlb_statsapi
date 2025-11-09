# Release Process

**IMPORTANT**: This project uses **automated CI/CD for releases**. Never manually publish to PyPI or create GitHub releases.

## Correct Release Workflow

### Prerequisites
1. All changes must be committed and pushed to `main`
2. All CI tests must pass (check GitHub Actions)
3. Ensure you're on the latest `main` branch

### Creating a Release

**Option 1: Using git.sh (Recommended)**

```bash
# For patch release (1.2.1 → 1.2.2)
bash scripts/git.sh release patch

# For minor release (1.2.2 → 1.3.0)
bash scripts/git.sh release minor

# For major release (1.3.0 → 2.0.0)
bash scripts/git.sh release major

# For custom version
bash scripts/git.sh release 1.5.0
```

**When prompted**, choose to push the tag to remote. This triggers the publish workflow.

**Option 2: Manual Tag Creation**

```bash
# Get current version
git describe --tags --abbrev=0

# Create new tag (e.g., v1.2.2)
git tag v1.2.2

# Push tag to trigger CI/CD
git push origin v1.2.2
```

### What Happens Automatically

When you push a tag matching `v*.*.*`:

1. **GitHub Actions Publish Workflow** (`.github/workflows/publish.yml`) triggers
2. Builds the package with `uv build`
3. Creates a **GitHub Release** with build artifacts
4. Publishes to **PyPI** using trusted publishing
5. Everything is versioned using `hatch-vcs` based on the git tag

### Monitoring the Release

```bash
# Check workflow status
gh run list --workflow=publish.yml

# Watch workflow in real-time
gh run watch
```

Or visit: https://github.com/power-edge/pymlb_statsapi/actions

### Post-Release Verification

```bash
# Verify GitHub release
gh release view v1.2.2

# Verify PyPI
pip index versions pymlb-statsapi
```

## What NOT to Do

❌ **NEVER** manually create GitHub releases
❌ **NEVER** manually publish to PyPI with `twine upload`
❌ **NEVER** create tags without pushing them (this creates sync issues)
❌ **NEVER** delete tags after pushing (breaks CI/CD state)

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes
- **MINOR** (x.Y.0): New features, backward compatible
- **PATCH** (x.y.Z): Bug fixes, backward compatible

Versions are automatically managed by `hatch-vcs` from git tags.

## Troubleshooting

### "Tag already exists"
```bash
# Delete local tag
git tag -d v1.2.2

# Delete remote tag (use with caution!)
git push --delete origin v1.2.2
```

### "Publish workflow didn't trigger"
1. Check tag format: Must be `vX.Y.Z` (lowercase 'v')
2. Verify tag is pushed: `git ls-remote --tags origin`
3. Check GitHub Actions permissions

### "PyPI upload failed"
1. Verify `PYPI_TOKEN` secret is configured
2. Ensure version doesn't already exist on PyPI
3. Check trusted publishing is configured

## Emergency: Rollback a Release

If a bad release was published:

1. **DO NOT** delete the git tag or GitHub release
2. Create a new patch release with the fix
3. For critical issues, yank the version on PyPI:
   ```bash
   # PyPI web interface → Manage → Yank this version
   ```

## CI/CD Configuration

The release automation is configured in:
- `.github/workflows/publish.yml` - Publish workflow
- `.github/workflows/ci-cd.yml` - Test workflow
- `pyproject.toml` - Build configuration with hatch-vcs
- `scripts/git.sh` - Helper script for releases

Never modify these without understanding the full impact on the release pipeline.
