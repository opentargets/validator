[![PyPI version](https://badge.fury.io/py/opentargets-validator.svg)](https://badge.fury.io/py/opentargets-validator)

[![Build Status](https://travis-ci.org/opentargets/validator.svg?branch=master)](https://travis-ci.org/opentargets/validator)

[![codecov](https://codecov.io/gh/opentargets/validator/branch/master/graph/badge.svg)](https://codecov.io/gh/opentargets/validator)

[![Docker Repository on Quay.io](https://quay.io/repository/opentargets/validator/status "Docker Repository on Quay.io")](https://quay.io/repository/opentargets/validator)

[![Anaconda-Server Badge](https://anaconda.org/bioconda/opentargets-validator/badges/version.svg)](https://anaconda.org/bioconda/opentargets-validator)

# opentargets-validator

Evidence string validator.

## Purpose

This tool is intended to validate JSON files that have a single JSON object per line. This is the format that is required from the [data sources](https://docs.targetvalidation.org/data-sources/data-sources) that provide us with evidence for our target-disease associations. 

The validator will check the expected structure, defined in a JSON schema which must be provided via a `--schema` argument. 

Be aware that this is *not* a general-purpose JSON validator, and use of "pretty-printed" JSON will cause errors. 

## Schema URLs
The Open Targets JSON schema is located at https://github.com/opentargets/json_schema. Note that you should *not* use `master` as this may change any time, instead use the latest available tag, e.g. `1.6.3`. If you are a data provider, you will always receive an email from Open Targets with information about what JSON schema version to use. Also, when specifying the schema to the validator you have to use the "raw" GitHub URL:

`https://raw.githubusercontent.com/opentargets/json_schema/1.6.3/opentargets.json`

## How to install it

The easiest way is with pip:

```sh
pip install -U opentargets-validator
```

It supports both Python 2 and Python 3.

You can also use Conda:

```sh
conda install -c bioconda opentargets-validator
```

## How to use it

You have two options:
- pass a filename or URL as a positional argument
- read from stdin (e.g. a shell pipe)

### Read from stdin

```sh
cat file.json | opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/{tag_version}/opentargets.json
```

### Read from positional argument

This can automatically decompress gzip'ed files. Compression will be detected via filename e.g. ending with `.json.gz`.

Examples of acceptable paths are:
- https://file/location/name.json
- https://file/location/name.json.gz
- file://relative/local/file.json
- file:///absolute/file.json
- location/file.json

```sh
opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/{tag_version}/opentargets.json https://where/myfile/is/located.json
```

## Note

There used to be a `--log-lines` argument that could be used to exit early when a certain number of errors occored. This is no longer supported, and with parallelization improvements it is rarely necessary in practice.

## How to develop 

Within a [virtualenv](https://virtualenv.pypa.io/en/latest/) you can install with:

```sh
pip install -e .[dev]
```

and you can run the tests with:

```sh
pytest --cov=opentargets_validator --cov-report term tests/ --fulltrace
```

This repository has [Travis integration](https://travis-ci.com/opentargets/validator) and [CodeCov integration](https://codecov.io/gh/opentargets/validator) .

Releases are put on [PyPI](https://pypi.org/project/opentargets-validator) automatically via Travis from GitHub tags.
