import concurrent.futures
import functools
import logging
import multiprocessing

import jsonschema
import pypeln
import simplejson as json

from .helpers import generate_validator_from_schema, box_text


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


def validate_start(schema_uri):
    validator = generate_validator_from_schema(schema_uri)
    logger = logging.getLogger(__name__)
    return dict(validator=validator, logger=logger)


def validator_mapped(data, validator, logger):
    line_counter, line = data
    try:
        parsed_line = json.loads(line)
    except Exception as e:
        logger.error('failed parsing line %i: %s %s', line_counter, line, e)
        return line_counter, None, None

    validation_errors = [(".".join(error.absolute_path), error.message) for error in validator.iter_errors(parsed_line)]

    return line_counter, validation_errors


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
        validity = list([f.result for f in concurrent.futures.as_completed(futures)])
        valid, invalid = len([v for v in validity if v]), len([v for v in validity if not v])

    logger.info(f'Processing is completed. Total {valid} valid records, {invalid} invalid records.')
    return invalid == 0



    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(validate_single_line_partial, validate_iterator)

    input_valid = True

    # Avoid problems due to pypeln behaving unexpectedly because of problematic input file, e.g. empty input file that crashes the enumerate call
    is_file_fine = False
    stage = pypeln.process.map(
        validator_mapped,
        enumerate(file_descriptor, start=1),
        on_start=functools.partial(validate_start, schema_uri),
        workers=cpus,
        maxsize=1000
    )

    for line_counter, validation_errors in stage:

        is_file_fine = True
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
