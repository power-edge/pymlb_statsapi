# Wiki Content Directory

This directory contains the markdown files for the GitHub Wiki.

## Structure

- `Home.md` - Wiki homepage with quick links
- `FAQ.md` - Frequently asked questions
- Additional pages can be added as needed

## Deployment

Wiki content is automatically deployed via GitHub Actions (`.github/workflows/wiki.yml`) when changes are pushed to the main branch.

## Local Development

Edit markdown files in this directory and commit them. The wiki will be updated automatically after pushing to main.

## Adding New Pages

1. Create a new `.md` file in this directory
2. Use a descriptive filename (e.g., `API-Reference.md`, `Contributing.md`)
3. Link to it from `Home.md` or other pages
4. Commit and push - the workflow will deploy it

## Manual Wiki Updates

You can also edit the wiki directly on GitHub at:
https://github.com/power-edge/pymlb_statsapi/wiki

However, those changes won't be tracked in this repository. We recommend making all changes here for version control.
