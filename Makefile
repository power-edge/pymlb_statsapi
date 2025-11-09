.PHONY: help install test lint format clean build docs serve-docs capture-stubs

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv sync --all-extras

test:  ## Run all tests (unit + BDD)
	uv run pytest tests/ -v
	uv run behave --tags @replay

test-unit:  ## Run unit tests only
	uv run pytest tests/ -v

test-bdd:  ## Run BDD tests only
	uv run behave --tags @replay

test-coverage:  ## Run tests with coverage
	uv run pytest tests/ --cov=pymlb_statsapi --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

lint:  ## Run linting checks
	uv run ruff check .

lint-fix:  ## Fix linting issues
	uv run ruff check --fix .

format:  ## Format code
	uv run ruff format .

security:  ## Run security checks
	uv run bandit -r pymlb_statsapi/ -ll

pre-commit:  ## Run all pre-commit hooks
	uv run pre-commit run --all-files

clean:  ## Clean build artifacts
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	uv build

docs:  ## Build documentation
	uv run sphinx-build -b html docs docs/_build/html
	@echo "Documentation: docs/_build/html/index.html"

serve-docs:  ## Serve documentation locally
	python -m http.server 8000 --directory docs/_build/html

capture-stubs:  ## Capture API stubs (respects rate limits)
	STUB_MODE=capture uv run python scripts/capture_all_stubs.py --delay 2

capture-stubs-behave:  ## Capture API stubs using behave
	STUB_MODE=capture uv run behave

publish-test:  ## Publish to TestPyPI
	uv run twine upload --repository testpypi dist/*

publish:  ## Publish to PyPI
	uv run twine upload dist/*

dev:  ## Set up development environment
	uv sync --all-extras
	uv run pre-commit install
	@echo "Development environment ready!"

check:  ## Run all checks (lint, format, test)
	@echo "Running linting..."
	uv run ruff check .
	@echo "Running format check..."
	uv run ruff format --check .
	@echo "Running security scan..."
	uv run bandit -r pymlb_statsapi/ -ll
	@echo "Running tests..."
	uv run pytest tests/ -v
	STUB_MODE=replay uv run behave
	@echo "All checks passed!"
