# Release Process

This document describes how to create releases for the Open Targets Validator package.

## Automated Release Process

The project uses GitHub Actions for automated releases to PyPI. There are two ways to create a release:

### Method 1: Create a Git Tag (Recommended)

1. **Update the version** in `opentargets_validator/version.py`:
   ```python
   __version__ = "1.0.2"  # Update to your new version
   ```

2. **Commit and push the changes**:
   ```bash
   git add opentargets_validator/version.py
   git commit -m "Bump version to 1.0.2"
   git push origin main
   ```

3. **Create and push a tag**:
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   ```

4. **GitHub Actions will automatically**:
   - Run tests on multiple Python versions (3.8-3.13)
   - Build the package
   - Create a GitHub release
   - Publish to PyPI

### Method 2: Manual Release via GitHub Actions

1. Go to the [Actions tab](https://github.com/opentargets/validator/actions) in the GitHub repository
2. Select "Create Release" workflow
3. Click "Run workflow"
4. Enter the version number (e.g., `1.0.2`)
5. Click "Run workflow"

The workflow will:
- Update the version in `version.py`
- Create a git tag
- Run tests and build the package
- Create a GitHub release
- Publish to PyPI

## Manual Release Process (Fallback)

If you need to release manually:

### Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies and build**:
   ```bash
   uv sync --dev
   uv build
   ```

3. **Check the package**:
   ```bash
   uv run twine check dist/*
   ```

4. **Upload to PyPI**:
   ```bash
   uv run twine upload dist/*
   ```

### Using pip (Legacy)

1. **Install build tools**:
   ```bash
   pip install build twine
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Check the package**:
   ```bash
   twine check dist/*
   ```

4. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

## PyPI Configuration

The project uses [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishing/) for secure, automated uploads. The configuration is handled through GitHub Actions with the `pypa/gh-action-pypi-publish` action.

### Setting up Trusted Publishing

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/publishing/)
2. Add a new pending publisher:
   - **PyPI Project**: `opentargets-validator`
   - **Owner**: `opentargets`
   - **Repository**: `validator`
   - **Workflow filename**: `python-publish.yml`
   - **Environment name**: `pypi`

3. The GitHub repository must have a `pypi` environment configured with appropriate protection rules.

## Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Examples:
- `1.0.0` → `1.0.1` (bug fix)
- `1.0.1` → `1.1.0` (new feature)
- `1.1.0` → `2.0.0` (breaking change)

## Development Workflow with uv

### Setting up the development environment

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

3. **Run tests**:
   ```bash
   uv run pytest
   ```

4. **Run linting**:
   ```bash
   uv run flake8 opentargets_validator tests
   uv run black --check opentargets_validator tests
   uv run isort --check-only opentargets_validator tests
   ```

5. **Build the package**:
   ```bash
   uv build
   ```

## Testing Before Release

Before creating a release, ensure:

1. **All tests pass**:
   ```bash
   uv run pytest
   ```

2. **Code quality checks pass**:
   ```bash
   uv run flake8 opentargets_validator tests
   uv run black --check opentargets_validator tests
   uv run isort --check-only opentargets_validator tests
   ```

3. **Package builds successfully**:
   ```bash
   uv build
   uv run twine check dist/*
   ```

4. **Documentation is up to date** (if applicable)

## Rollback Process

If a release needs to be rolled back:

1. **Remove the tag** (if not yet published):
   ```bash
   git tag -d v1.0.2
   git push origin :refs/tags/v1.0.2
   ```

2. **Delete the GitHub release** (if created)

3. **Contact PyPI support** if the package was already uploaded to PyPI

## Troubleshooting

### Common Issues

1. **Version mismatch**: Ensure the version in `version.py` matches the git tag
2. **Build failures**: Check that all dependencies are properly specified
3. **PyPI upload failures**: Verify trusted publishing is configured correctly
4. **Test failures**: Ensure all tests pass before creating a release

### Getting Help

- Check the [GitHub Actions logs](https://github.com/opentargets/validator/actions)
- Review the [PyPI documentation](https://packaging.python.org/)
- Contact the maintainers via [GitHub Issues](https://github.com/opentargets/validator/issues)
