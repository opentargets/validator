[![PyPI version](https://badge.fury.io/py/opentargets-validator.svg)](https://badge.fury.io/py/opentargets-validator)

[![Build Status](https://travis-ci.org/opentargets/validator.svg?branch=master)](https://travis-ci.org/opentargets/validator)

[![codecov](https://codecov.io/gh/opentargets/validator/branch/master/graph/badge.svg)](https://codecov.io/gh/opentargets/validator)

[![Docker Repository on Quay.io](https://quay.io/repository/opentargets/validator/status "Docker Repository on Quay.io")](https://quay.io/repository/opentargets/validator)

# opentargets-validator

Evidence string validator.

## Purpose

This tool is intended to validate JSON files that have a single JSON object per line. This is the format that is required from the [data sources](https://docs.targetvalidation.org/data-sources/data-sources) that provide us with evidence for our target-disease associations. 

The validator will check the expected structure, look for missing objects, flag disease IDs that do not start as EFO and Orphanet ID, among other assessments.

Be aware that this is *not* a general-purpose JSON validator, and use of "pretty-printed" JSON will cause errors. 

### Schema URLs

The OpenTargets JSON schema is located at https://github.com/opentargets/json_schema/blob/master/opentargets.json . When specifying this schema to the validator, you should use the "raw" GitHub URL, e.g. 

`https://raw.githubusercontent.com/opentargets/json_schema/1.5.0/opentargets.json`

Also to make sure that the version tag (1.5.0 in the example above) corresponds with the version you wish to use; for example you may want to use `master` to get the absolute latest version.

## How to install it

```sh
pip install opentargets-validator
```

## How to use it

You have two options
- read from a stdin file (_piped_ one)
- pass as a positional argument and use a zipped or gzipped file (optional)

### Read from stdin

```sh
cat file.json | opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/1.5.0/opentargets.json
```
All log messages will be redirected to _stderr_.

### Read from positional argument

Filename extensions could be `.[json|json.zip|json.zip]`

Using this option you could use these uri formats
- http[s]://file/location/name.json
- file://relative/local/file.json
- file:///absolute/file.json
- location/file.json

```sh
opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/1.5.0/opentargets.json https://where/myfile/is/located.json
```

### How many lines do you want to get printed?

Using the parameter `--log-lines 100`, `opentargets_validator` will accumulate up to
100 lines and then it will exit.

## How to develop it

Within a [virtualenv](https://virtualenv.pypa.io/en/latest/) you can install with:

```sh
pip install -e .[dev]
```

and you can run the tests with:

```sh
pytest --cov=opentargets_validator --cov-report term tests/ --fulltrace
```

This repository has [Travis integration](https://travis-ci.com/opentargets/validator) and [CodeCov integration](https://codecov.io/gh/opentargets/validator) .

Releases are put on [PyPI](https://pypi.org/project/opentargets-validator).
