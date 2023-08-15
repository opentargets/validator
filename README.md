[![PyPI version](https://badge.fury.io/py/opentargets-validator.svg)](https://badge.fury.io/py/opentargets-validator)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/opentargets-validator/badges/version.svg)](https://anaconda.org/bioconda/opentargets-validator)
[![Build Status](https://travis-ci.org/opentargets/validator.svg?branch=master)](https://travis-ci.org/opentargets/validator)
[![Docker Repository on Quay.io](https://quay.io/repository/opentargets/validator/status "Docker Repository on Quay.io")](https://quay.io/repository/opentargets/validator)
[![codecov](https://codecov.io/gh/opentargets/validator/branch/master/graph/badge.svg)](https://codecov.io/gh/opentargets/validator)

# Open Targets JSON validator
The `opentargets-validator` tool in this repository validates JSON files which are submitted to Open Targets by various [data sources](https://docs.targetvalidation.org/data-sources/data-sources) against the Open Targets [JSON schemas](https://github.com/opentargets/json_schema).

## Installation
```bash
pip install --upgrade opentargets-validator
```

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

Each input file can be read from:
* STDIN (`-`)
* Uncompressed remote file (https://example.com/example.json)
* Uncompressed local file (`example.json`)
* GZIP-compressed local file (`example.json.gz`)

## Development instructions 
An editable copy can be installed within a [virtualenv](https://virtualenv.pypa.io/en/latest/):
```bash
pip install -e .[dev]
```

The tests can be run with:
```sh
pytest --cov=opentargets_validator --cov-report term tests/ --fulltrace
```

This repository has [Travis integration](https://travis-ci.com/opentargets/validator) and [CodeCov integration](https://codecov.io/gh/opentargets/validator).

Releases are put on [PyPI](https://pypi.org/project/opentargets-validator) automatically via Travis from GitHub tags.
