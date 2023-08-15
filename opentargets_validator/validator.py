import copy
from itertools import islice
import json
import logging
import concurrent.futures
import pathos.multiprocessing
import fastjsonschema

from .helpers import box_text


def validate_single_line(line_number, line, validator, logger):
    def format_error(error_type):
        logger.error(f'Line #{line_number} {error_type}. Error:\n{box_text(str(e))}\n{line}\n\n\n')

    # Lines come directly from file object-like iterators, so we should strip the end of line characters.
    line = line.rstrip()

    # Does the line contain a valid JSON object at all?
    try:
        parsed_line = json.loads(line)
    except Exception as e:
        format_error('is not a valid JSON object')
        return False

    # Does the JSON object in the line validate against the schema?
    try:
        validator(parsed_line)
    except Exception as e:
        format_error('is a valid JSON object, but it does not match the schema')
        return False

    return True


def validate(data_fd, schema_fd):
    logger = logging.getLogger(__name__)

    # Load the schema and check if it is itself valid.
    try:
        schema_contents = json.load(schema_fd)
    except Exception as e:
        logger.error(f'JSON schema is not valid. Error: ~~~{e}~~~.')
        return False

    # Compile the validator.
    validator = fastjsonschema.compile(schema_contents)

    # Validate all input lines concurrently.
    with pathos.multiprocessing.ProcessingPool(processes=pathos.multiprocessing.cpu_count()) as pool:
        validity = pool.map(
            lambda args: validate_single_line(*args),
            [(line_number, line, validator, logger)
             for line_number, line in enumerate(data_fd, 1)]
        )

    # Process the results.
    valid, invalid = len([v for v in validity if v]), len([v for v in validity if not v])
    logger.info(f'Processing is completed. Total {valid} valid records, {invalid} invalid records.')
    return invalid == 0
