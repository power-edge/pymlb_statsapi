# GitHub Wiki Infrastructure Management
#
# Note: GitHub wikis are Git repositories themselves.
# Wiki content is managed in /wiki directory and can be deployed manually.
#
# To enable wiki:
# 1. Update main.tf: Change `has_wiki = false` to `has_wiki = true`
# 2. Run: terraform apply
# 3. Manually initialize wiki with content from /wiki directory
#
# The wiki feature is enabled in main.tf (github_repository.settings)
