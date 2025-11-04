## Description

<!-- Provide a brief description of what this PR accomplishes -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition or modification
- [ ] CI/CD or build changes

## Related Issues

<!-- Link to related issues using #issue_number -->

Closes #
Related to #

## Changes Made

<!-- Provide a detailed list of changes -->

-
-
-

## Testing

<!-- Describe the tests you ran and their results -->

### Test Coverage

- [ ] Unit tests added/updated
- [ ] BDD tests added/updated
- [ ] All existing tests pass
- [ ] Test coverage maintained or improved

### Test Commands Run

```bash
# List the commands you ran to test these changes
uv run pytest
STUB_MODE=replay uv run behave
```

### Test Results

<!-- Paste relevant test output or describe results -->

```
# Paste test output here
```

## Code Quality Checklist

<!-- Verify all items before submitting -->

- [ ] Code follows the project's coding standards
- [ ] Linting passes (`uv run ruff check .`)
- [ ] Formatting passes (`uv run ruff format --check .`)
- [ ] Type checking passes (`uv run mypy pymlb_statsapi/`)
- [ ] Security scan passes (`uv run bandit -r pymlb_statsapi/ -ll`)
- [ ] Pre-commit hooks pass (`uv run pre-commit run --all-files`)
- [ ] No new warnings introduced
- [ ] Branch is up-to-date with main

## Documentation

<!-- Mark all that apply -->

- [ ] Docstrings added/updated for new/modified functions
- [ ] README.md updated (if applicable)
- [ ] CHANGELOG.md updated (for notable changes)
- [ ] Schema reference documentation updated (if schemas changed)
- [ ] Examples added/updated (if applicable)
- [ ] API documentation reviewed

## Schema Changes

<!-- If you modified schemas, describe the changes -->

- [ ] No schema changes
- [ ] Schema changes (describe below):

<!--
Describe schema modifications:
- Which schemas were modified?
- Why were the changes necessary?
- Are these breaking changes?
-->

## Breaking Changes

<!-- If this includes breaking changes, describe them -->

- [ ] No breaking changes
- [ ] Breaking changes (describe below):

<!--
Describe breaking changes:
- What will break?
- How should users migrate?
- Have you updated the version accordingly?
-->

## Screenshots / Examples

<!-- If applicable, add screenshots or code examples -->

### Before

```python
# Code before changes (if applicable)
```

### After

```python
# Code after changes (if applicable)
```

## Performance Impact

<!-- Describe any performance implications -->

- [ ] No performance impact
- [ ] Performance improved
- [ ] Performance degraded (explain justification below)

<!-- If performance is affected, provide details -->

## Deployment Notes

<!-- Any special deployment considerations? -->

- [ ] No special deployment steps required
- [ ] Special deployment steps (describe below):

<!-- Describe any special deployment requirements -->

## Additional Context

<!-- Add any other context about the PR here -->

## Reviewer Notes

<!-- Any specific areas you'd like reviewers to focus on? -->

---

## Checklist for Reviewers

<!-- Reviewers: Please verify the following -->

- [ ] Code changes are clear and well-documented
- [ ] Tests adequately cover the changes
- [ ] Documentation is accurate and complete
- [ ] No obvious security issues
- [ ] Performance implications are acceptable
- [ ] Breaking changes are justified and documented
- [ ] Code follows project conventions
