from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
import logging
import simplejson as json
import multiprocessing
from .helpers import generate_validator_from_schema
import pypeln
import functools


def validate_start(schema_uri):
    validator = generate_validator_from_schema(schema_uri)
    logger = logging.getLogger(__name__)
    return validator, logger

def validator_mapped(data, validator, logger):
    line_counter, line = data
    try:
        parsed_line = json.loads(line)
    except Exception as e:
        logger.error('failed parsing line %i: %s %s', line_counter, line, e)
        return line_counter, None, None

    validation_errors = [(".".join(error.absolute_path), error.message) for error in validator.iter_errors(parsed_line)]

    return line_counter, validation_errors

def validate(file_descriptor, schema_uri):
    logger = logging.getLogger(__name__)
    input_valid = True

    cpus = multiprocessing.cpu_count()

    # Avoid problems due to pypeln behaving unexpectedly because of problematic input file, e.g. empty input file that crashes the enumerate call
    is_file_fine=False
    stage = pypeln.process.map(validator_mapped, enumerate(file_descriptor, start=1),
        on_start=functools.partial(validate_start, schema_uri),
        workers=cpus,
        maxsize=1000)

    for line_counter, validation_errors in stage:
        is_file_fine=True
        line_valid = True

        if validation_errors:
            line_valid = False
            input_valid = False
            for path, message in validation_errors:
                logger.error('fail @ %i.%s %s', line_counter, path, message)


    # If there were issues with input file, e.g. because it was empty, flag it
    if not is_file_fine:
        logger.error("Issue with input file, probably because it was empty")
        input_valid = False

    return input_valid
