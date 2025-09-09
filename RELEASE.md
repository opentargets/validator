# Release Process

This document describes how to create releases for the Open Targets Validator package.

## Automated Release Process

The project uses GitHub Actions for automated releases to PyPI. The `build-release` workflow is triggered when a GitHub release is published.

### Method 1: Using the Version Bump Script (Recommended)

1. **Use the automated version bump script**:
   ```bash
   python3 scripts/bump_version.py 1.0.2
   ```

   This script will:
   - Update the version in `opentargets_validator/version.py`
   - Update the version in `pyproject.toml` (if present)
   - Validate the version format (semantic versioning)
   - Provide next steps for creating the release

2. **Follow the script's instructions**:
   ```bash
   git add opentargets_validator/version.py pyproject.toml
   git commit -m "Bump version to 1.0.2"
   git tag v1.0.2
   git push origin main
   git push origin v1.0.2
   ```

3. **Create a GitHub Release**:
   - Go to the [Releases page](https://github.com/opentargets/validator/releases)
   - Click "Create a new release"
   - Choose the tag `v1.0.2`
   - Add release notes
   - Click "Publish release"

4. **GitHub Actions will automatically**:
   - Run tests and linting
   - Build the package
   - Publish to PyPI using trusted publishing

### Method 2: Manual Version Update

1. **Update the version** in `opentargets_validator/version.py`:
   ```python
   __version__ = "1.0.2"  # Update to your new version
   ```

2. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   version = "1.0.2"
   ```

3. **Commit and push the changes**:
   ```bash
   git add opentargets_validator/version.py pyproject.toml
   git commit -m "Bump version to 1.0.2"
   git push origin main
   ```

4. **Create and push a tag**:
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   ```

5. **Create a GitHub Release** (same as Method 1, step 3)

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
   - **Workflow filename**: `build-release.yaml`
   - **Environment name**: `pypi` (optional - currently commented out)

3. The GitHub repository should have a `pypi` environment configured with appropriate protection rules (currently commented out in the workflow).

### Current Workflow Configuration

The `build-release.yaml` workflow:
- Triggers on GitHub release publication
- Runs tests and linting using `uv`
- Builds the package using `uv build`
- Publishes to PyPI using trusted publishing
- Uses `ubuntu-22.04` runners
- Includes proper caching for faster builds

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

4. **Run linting and formatting**:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   ```

5. **Build the package**:
   ```bash
   uv build
   ```

6. **Check package integrity**:
   ```bash
   uv run twine check dist/*
   ```

## Testing Before Release

Before creating a release, ensure:

1. **All tests pass**:
   ```bash
   uv run pytest
   ```

2. **Code quality checks pass**:
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   ```

3. **Package builds successfully**:
   ```bash
   uv build
   uv run twine check dist/*
   ```

4. **Version bump script works** (if using Method 1):
   ```bash
   python3 scripts/bump_version.py 1.0.2
   ```

5. **Documentation is up to date** (if applicable)

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

1. **Version mismatch**: Ensure the version in `version.py` and `pyproject.toml` matches the git tag
2. **Build failures**: Check that all dependencies are properly specified in `pyproject.toml`
3. **PyPI upload failures**: Verify trusted publishing is configured correctly
4. **Test failures**: Ensure all tests pass before creating a release
5. **Linting failures**: Run `uv run ruff check .` and fix any issues
6. **Version bump script errors**: Ensure the version follows semantic versioning (e.g., `1.0.2`)

### Getting Help

- Check the [GitHub Actions logs](https://github.com/opentargets/validator/actions)
- Review the [PyPI documentation](https://packaging.python.org/)
- Check the [uv documentation](https://docs.astral.sh/uv/)
- Contact the maintainers via [GitHub Issues](https://github.com/opentargets/validator/issues)
