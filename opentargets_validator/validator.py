from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
import logging
import simplejson as json
import multiprocessing
import hashlib
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
        logger.error('failed parsing line %i: %s', line_counter, e)
        return line_counter, None, None

    validation_errors = [(".".join(error.absolute_path), error.message) for error in validator.iter_errors(parsed_line)]

    hash_line = hashlib.md5(json.dumps(parsed_line["unique_association_fields"], 
        sort_keys=True).encode("utf-8")).hexdigest()

    return line_counter, validation_errors, hash_line

def validate(file_descriptor, schema_uri, do_hash):
    logger = logging.getLogger(__name__)
    hash_lines = dict()
    input_valid = True

    cpus = multiprocessing.cpu_count()

    stage = pypeln.process.map(validator_mapped, enumerate(file_descriptor, start=1),
        on_start=functools.partial(validate_start, schema_uri),
        workers=cpus,
        maxsize=1000)

    for line_counter, validation_errors, hash_line in stage:
        line_valid = True

        if validation_errors:
            line_valid = False
            input_valid = False
            for path, message in validation_errors:
                logger.error('fail @ %i.%s %s', line_counter, path, message)


        #check for any hash collisions
        #only check those that have passed validation so far
        if do_hash and line_valid:
            if hash_line in hash_lines:
                #duplicate hash, fail this line
                line_valid = False
                input_valid = False

                # order the lies so log is sensible
                # might not be ordered due to pypeln multiprocessing
                line_min = min(line_counter, hash_lines[hash_line])
                line_max = max(line_counter, hash_lines[hash_line])
                logger.error("Duplicate hashes %d and %d ",
                    line_min, line_max)
            else:
                hash_lines[hash_line] = line_counter

        line_counter += 1

    #check if we had no lines, if so something went wrong and needs to be flagged
    if line_counter == 0:
        logger.error("No lines in input - does it exist?")
        input_valid = False

    return input_valid
