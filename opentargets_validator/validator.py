from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
import time
import logging
import json
import codecs
from sys import exit
from .helpers import generate_validator_from_schema


def validate(file_descriptor, schema_uri, loglines):
    logger = logging.getLogger(__name__)
    error_lines = abs(loglines)
    line_counter = 1
    parsed_line = None
    valid = True

    validator = generate_validator_from_schema(schema_uri)

    for line in file_descriptor:
        try:
            parsed_line = json.loads(line)
        except Exception as e:
            logger.error('failed parsing line %i: %s', line_counter, e)

        validation_errors = [error for error in validator.iter_errors(parsed_line)]

        if validation_errors:
            valid = False
            for validation_error in validation_errors:
                logger.error('fail @ %i.%s %s',
                    line_counter, ".".join(validation_error.absolute_path), validation_error.message)

            error_lines -= 1
            if error_lines <= 0:
                break #end the for loop early

        line_counter += 1

    return valid
