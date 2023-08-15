import concurrent.futures
import json
import logging
import multiprocessing

import jsonschema

from .helpers import box_text


def validate_single_line(line_number, line, schema, logger):
    def format_error(error_type):
        logger.error(f'Line #{line_number} {error_type}. Error:\n{box_text(str(e))}\nFull line: {line}\n\n\n')

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
        jsonschema.validate(instance=parsed_line, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        format_error('is a valid JSON object, but it does not match the schema')
        return False

    return True


def validate(data_fd, schema_fd):
    logger = logging.getLogger(__name__)

    # Load the schema and check if it is itself valid.
    try:
        schema = json.load(schema_fd)
    except Exception as e:
        logger.error('JSON schema is not valid. Error: ~~~{e}~~~.')
        return False

    # Validate all input lines concurrently.
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        # Submit the calculations.
        futures = [
            executor.submit(validate_single_line, line_number, line, schema, logger)
            for line_number, line in enumerate(data_fd, 1)
        ]
        # Process results.
        validity = list([f.result() for f in concurrent.futures.as_completed(futures)])
        valid, invalid = len([v for v in validity if v]), len([v for v in validity if not v])

    logger.info(f'Processing is completed. Total {valid} valid records, {invalid} invalid records.')
    return invalid == 0
