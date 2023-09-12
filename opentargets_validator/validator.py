import itertools
import json
import logging
import pathos.multiprocessing
import fastjsonschema

from .helpers import box_text


def validate_block_of_lines(list_of_lines_with_indexes, validator, logger):
    def format_error(error_type, e):
        logger.error(f"\nLine #{line_index} {error_type}:\n{box_text(str(e))}\n{line}\n\n\n")

    valid, invalid = 0, 0

    for line_index, line in list_of_lines_with_indexes:
        # Lines come directly from file object-like iterators, so we should strip the end of line characters.
        line = line.rstrip()

        # Does the line contain a valid JSON object at all?
        try:
            parsed_line = json.loads(line)
        except Exception as e:
            format_error("is not a valid JSON object", e)
            invalid += 1
            continue

        # Does the JSON object in the line validate against the schema?
        try:
            validator(parsed_line)
        except Exception as e:
            format_error("is a valid JSON object, but it does not match the schema", e)
            invalid += 1
            continue

        valid += 1

    return valid, invalid


def batch_iterator(iterator, batch_size=5000):
    """Convert an iterator into another iterator that returns blocks of a specified batch size."""
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def validate(data_fd, schema_fd):
    logger = logging.getLogger(__name__)

    # Load the schema and check if it is itself valid.
    try:
        schema_contents = json.load(schema_fd)
    except Exception as e:
        logger.error(f"JSON schema is not valid. Error: ~~~{e}~~~.")
        return False

    # Compile the validator.
    validator = fastjsonschema.compile(schema_contents)

    # Line by line iterator.
    line_iterator = data_fd
    # Enumerate to keep track of line numbers.
    enumerated_iterator = enumerate(line_iterator, 1)
    # Package previous iterator into blocks of multiple lines to increase performance.
    blocked_iterator = batch_iterator(enumerated_iterator)
    # Final argument list iterator.
    args_list_iterator = ([line_block, validator, logger] for line_block in blocked_iterator)

    # Validate all input lines concurrently.
    with pathos.multiprocessing.ProcessPool(processes=pathos.multiprocessing.cpu_count()) as pool:
        validity = list(pool.imap(
            lambda args: validate_block_of_lines(*args),
            args_list_iterator,
        ))

    # Process the results.
    valid, invalid = sum([v[0] for v in validity]), sum([v[1] for v in validity])
    logger.info(f"Processing is completed. Total {valid} valid records, {invalid} invalid records.")
    return invalid == 0
