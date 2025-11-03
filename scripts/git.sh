#!/bin/bash
set -e

# Usage: ./git.sh [command] [options]
# Commands:
#   status              - Show git status
#   commit [msg]        - Format, check, and commit with optional message
#   release [version]   - Create release tag (patch/minor/major/X.Y.Z)
#   push [--tags]       - Push to remote
#   full [version]      - Full release workflow
#
# Examples:
#   ./git.sh commit "feat: add new feature"
#   ./git.sh release minor
#   ./git.sh release 1.0.0
#   ./git.sh full 1.0.0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Check if there are uncommitted changes
check_status() {
    if [[ -n $(git status -s) ]]; then
        return 0  # Has changes
    else
        return 1  # No changes
    fi
}

# Get current version from git tags
get_current_version() {
    local version=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    echo "${version#v}"  # Remove 'v' prefix
}

# Bump version
bump_version() {
    local version=$1
    local bump_type=$2

    IFS='.' read -r -a parts <<< "$version"
    local major="${parts[0]}"
    local minor="${parts[1]}"
    local patch="${parts[2]}"

    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Invalid bump type"
            exit 1
            ;;
    esac

    echo "${major}.${minor}.${patch}"
}

# Main menu
show_menu() {
    echo ""
    echo "================================"
    echo "   Git Workflow Helper"
    echo "================================"
    echo "1) Format & commit changes"
    echo "2) Create release (bump version & tag)"
    echo "3) Push to remote"
    echo "4) Full release (format, commit, bump, tag, push, build)"
    echo "5) Status"
    echo "6) Exit"
    echo "================================"
    read -r -p "Choose an option: " choice
    echo ""

    case $choice in
        1) format_and_commit ;;
        2) create_release ;;
        3) push_to_remote ;;
        4) full_release ;;
        5) show_status ;;
        6) exit 0 ;;
        *)
            print_error "Invalid option"
            show_menu
            ;;
    esac
}

# Show git status
show_status() {
    print_step "Git status:"
    git status -sb
    echo ""

    local current_version=$(get_current_version)
    print_step "Current version: v${current_version}"

    echo ""
    read -r -p "Press Enter to continue..."
    show_menu
}

# Format and commit with commitizen format
format_and_commit() {
    if ! check_status; then
        print_warning "No changes to commit"
        show_menu
        return
    fi

    print_step "Running ruff format..."
    uv run ruff format .

    print_step "Running ruff check --fix..."
    uv run ruff check --fix .

    print_step "Staging changes..."
    git add -u

    print_step "Running pre-commit hooks..."
    if uv run pre-commit run --all-files; then
        print_success "Pre-commit checks passed"
    else
        print_warning "Pre-commit made changes, staging them..."
        git add -u
    fi

    echo ""
    print_step "Current changes:"
    git status -s
    echo ""

    # Commitizen format helper
    echo "Commit type:"
    echo "  feat:     A new feature"
    echo "  fix:      A bug fix"
    echo "  docs:     Documentation changes"
    echo "  style:    Code style changes (formatting, etc)"
    echo "  refactor: Code refactoring"
    echo "  perf:     Performance improvements"
    echo "  test:     Adding or updating tests"
    echo "  build:    Build system changes"
    echo "  ci:       CI/CD changes"
    echo "  chore:    Other changes (maintenance, etc)"
    echo ""

    read -r -p "Commit type: " commit_type
    read -r -p "Scope (optional, press enter to skip): " commit_scope
    read -r -p "Short description: " commit_desc

    if [[ -z "$commit_type" ]] || [[ -z "$commit_desc" ]]; then
        print_error "Type and description are required"
        show_menu
        return
    fi

    # Build commit message
    if [[ -n "$commit_scope" ]]; then
        commit_msg="${commit_type}(${commit_scope}): ${commit_desc}"
    else
        commit_msg="${commit_type}: ${commit_desc}"
    fi

    echo ""
    print_step "Commit message: ${commit_msg}"
    read -r -p "Proceed? (y/n): " confirm

    if [[ $confirm != "y" ]]; then
        print_warning "Cancelled"
        show_menu
        return
    fi

    git commit -m "$commit_msg"
    print_success "Changes committed"

    echo ""
    read -r -p "Return to menu? (y/n): " continue
    if [[ $continue == "y" ]]; then
        show_menu
    fi
}

# Create release (bump version and tag)
create_release() {
    local current_version=$(get_current_version)

    print_step "Current version: v${current_version}"
    echo ""
    echo "Select version bump type:"
    echo "1) Patch (${current_version} -> $(bump_version $current_version patch))"
    echo "2) Minor (${current_version} -> $(bump_version $current_version minor))"
    echo "3) Major (${current_version} -> $(bump_version $current_version major))"
    echo "4) Custom version"
    echo "5) Cancel"

    read -r -p "Choose: " bump_choice

    local new_version
    case $bump_choice in
        1) new_version=$(bump_version $current_version patch) ;;
        2) new_version=$(bump_version $current_version minor) ;;
        3) new_version=$(bump_version $current_version major) ;;
        4)
            read -r -p "Enter custom version (e.g., 1.2.3): " new_version
            ;;
        5)
            show_menu
            return
            ;;
        *)
            print_error "Invalid choice"
            create_release
            return
            ;;
    esac

    print_step "Creating tag v${new_version}..."
    git tag "v${new_version}"
    print_success "Tag created: v${new_version}"

    echo ""
    read -r -p "Push tag to remote? (y/n): " push_tag
    if [[ $push_tag == "y" ]]; then
        git push --tags
        print_success "Tag pushed to remote"
    fi

    echo ""
    read -r -p "Build package? (y/n): " do_build
    if [[ $do_build == "y" ]]; then
        print_step "Building package..."
        uv build
        print_success "Package built"
    fi

    echo ""
    read -r -p "Return to menu? (y/n): " continue
    if [[ $continue == "y" ]]; then
        show_menu
    fi
}

# Push to remote
push_to_remote() {
    print_step "Pushing to remote..."

    local current_branch=$(git branch --show-current)
    print_step "Current branch: ${current_branch}"

    echo ""
    echo "1) Push current branch"
    echo "2) Push with tags"
    echo "3) Force push (use with caution!)"
    echo "4) Cancel"

    read -r -p "Choose: " push_choice

    case $push_choice in
        1)
            git push
            print_success "Pushed to remote"
            ;;
        2)
            git push && git push --tags
            print_success "Pushed with tags"
            ;;
        3)
            read -r -p "Are you sure you want to force push? (yes/n): " confirm
            if [[ $confirm == "yes" ]]; then
                git push --force
                print_success "Force pushed"
            else
                print_warning "Cancelled"
            fi
            ;;
        4)
            show_menu
            return
            ;;
        *)
            print_error "Invalid choice"
            push_to_remote
            return
            ;;
    esac

    echo ""
    read -r -p "Return to menu? (y/n): " continue
    if [[ $continue == "y" ]]; then
        show_menu
    fi
}

# Full release workflow
full_release() {
    print_step "Starting full release workflow..."
    echo ""

    # Step 1: Check for changes
    if check_status; then
        print_warning "You have uncommitted changes"
        read -r -p "Commit them now? (y/n): " do_commit
        if [[ $do_commit == "y" ]]; then
            format_and_commit
        else
            print_error "Cannot create release with uncommitted changes"
            show_menu
            return
        fi
    fi

    # Step 2: Create release
    create_release

    print_success "Full release workflow completed!"
    echo ""
    read -r -p "Return to menu? (y/n): " continue
    if [[ $continue == "y" ]]; then
        show_menu
    fi
}

# Non-interactive mode (command-line arguments)
if [[ $# -gt 0 ]]; then
    command=$1
    shift  # Remove first argument

    case $command in
        status)
            print_step "Git status:"
            git status -sb
            echo ""
            current_version=$(get_current_version)
            print_step "Current version: v${current_version}"
            ;;

        commit)
            if ! check_status; then
                print_warning "No changes to commit"
                exit 0
            fi

            print_step "Running ruff format..."
            uv run ruff format .

            print_step "Running ruff check --fix..."
            uv run ruff check --fix .

            print_step "Staging changes..."
            git add -u

            print_step "Running pre-commit hooks..."
            if uv run pre-commit run --all-files; then
                print_success "Pre-commit checks passed"
            else
                print_warning "Pre-commit made changes, staging them..."
                git add -u
            fi

            if [[ $# -gt 0 ]]; then
                # Commit message provided
                commit_msg="$1"
                git commit -m "$commit_msg"
                print_success "Changes committed: $commit_msg"
            else
                # Fall back to interactive mode for commit message
                format_and_commit
            fi
            ;;

        release)
            current_version=$(get_current_version)

            if [[ $# -gt 0 ]]; then
                version_arg="$1"
                case $version_arg in
                    patch|minor|major)
                        new_version=$(bump_version $current_version $version_arg)
                        ;;
                    *)
                        # Assume it's a version number
                        new_version="$version_arg"
                        ;;
                esac
            else
                print_error "Version argument required (patch/minor/major/X.Y.Z)"
                exit 1
            fi

            print_step "Creating tag v${new_version}..."
            git tag "v${new_version}"
            print_success "Tag created: v${new_version}"

            # Check for --push or --build flags
            for arg in "$@"; do
                case $arg in
                    --push)
                        git push --tags
                        print_success "Tag pushed to remote"
                        ;;
                    --build)
                        print_step "Building package..."
                        uv build
                        print_success "Package built"
                        ;;
                esac
            done
            ;;

        push)
            current_branch=$(git branch --show-current)
            print_step "Pushing branch: ${current_branch}"

            if [[ "$1" == "--tags" ]]; then
                git push && git push --tags
                print_success "Pushed with tags"
            else
                git push
                print_success "Pushed to remote"
            fi
            ;;

        full)
            print_step "Starting full release workflow..."

            # Step 1: Commit if there are changes
            if check_status; then
                print_warning "Committing changes..."
                bash "$0" commit "chore: prepare for release"
            fi

            # Step 2: Create release
            if [[ $# -gt 0 ]]; then
                bash "$0" release "$1" --push --build
            else
                print_error "Version argument required for full release"
                exit 1
            fi

            print_success "Full release workflow completed!"
            ;;

        help|--help|-h)
            head -16 "$0" | tail -12
            ;;

        *)
            print_error "Unknown command: $command"
            echo ""
            head -16 "$0" | tail -12
            exit 1
            ;;
    esac
else
    # Interactive mode (original behavior)
    clear
    show_menu
fi
