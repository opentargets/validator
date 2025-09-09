[![PyPI version](https://badge.fury.io/py/opentargets-validator.svg)](https://badge.fury.io/py/opentargets-validator)
[![CI](https://github.com/opentargets/validator/workflows/CI/badge.svg)](https://github.com/opentargets/validator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/opentargets/validator/branch/master/graph/badge.svg)](https://codecov.io/gh/opentargets/validator)

# Open Targets JSON validator
The `opentargets-validator` tool in this repository validates JSON files which are submitted to Open Targets by various [data sources](https://docs.targetvalidation.org/data-sources/data-sources) against the Open Targets [JSON schemas](https://github.com/opentargets/json_schema).

## Installation
```bash
pip install --upgrade opentargets-validator
```

## Requirements
- Python 3.8.1 or higher
- Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13

## Usage examples
Validating a local gzipped file against the latest schema version from GitHub:
```bash
opentargets_validator \
  --schema https://raw.githubusercontent.com/opentargets/json_schema/master/schemas/disease_target_evidence.json \
  evidence.json.gz
```

Validating a portion of the local file against a local copy of the schema:
```bash
zcat evidence.json.gz | head -n 100 | opentargets_validator --schema evidence_schema.json
```

## Input files
The validator has to be provided with two inputs:
1. Data to validate. It has to contain exactly one complete JSON object per line.
2. Schema to validate against. It can be any valid JSON Draft 7 schema.

Either of the input files (data and schema) can be read from:
* STDIN (`-`)
* Uncompressed remote file (https://example.com/example.json)
* Uncompressed local file (`example.json`)
* GZIP-compressed local file (`example.json.gz`)

## Development

### Quick start with uv (recommended)
```bash
# Install uv and dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync --dev

# Run tests and linting
uv run pytest
uv run ruff check opentargets_validator tests
```

### Using pip
```bash
python -m venv env && source env/bin/activate
pip install -e ".[dev]"
python -m pytest
```

## CI/CD and Releases

This repository uses [GitHub Actions](https://github.com/opentargets/validator/actions) for continuous integration and [CodeCov](https://codecov.io/gh/opentargets/validator) for coverage reporting.

Releases are automatically published to [PyPI](https://pypi.org/project/opentargets-validator) via GitHub Actions when tags are created.

## Modern Python Tooling

This project has been modernized with:
- **`uv`** for fast dependency management and builds
- **`ruff`** for lightning-fast linting and formatting
- **`hatchling`** as the modern build backend
- **`importlib.resources`** instead of deprecated `pkg_resources`
- **GitHub Actions** for CI/CD instead of Travis CI
- **`pyproject.toml`** for modern Python project configuration
