[![Build Status](https://travis-ci.org/opentargets/validator.svg?branch=master)](https://travis-ci.org/opentargets/validator)
[![codecov](https://codecov.io/gh/opentargets/validator/branch/master/graph/badge.svg)](https://codecov.io/gh/opentargets/validator)

# opentargets-validator

Evidence string validator.

## Purpose

This validator is intended to validate JSON files that have a single JSON object per line. This is the format that is required from evidence submitters. As such it is *not* a general-purpose JSON validator, and use of "pretty-printed" JSON will cause errors.

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
cat file.json | opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/master/src/literature_curated.json
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
opentargets_validator --schema https://raw.githubusercontent.com/opentargets/json_schema/master/src/literature_curated.json https://where/myfile/is/located.json
```

### How many lines do you want to get printed?

Using the parameter `--log-lines 100`, `opentargets_validator` will accumulate up to
100 lines and then it will exit.
