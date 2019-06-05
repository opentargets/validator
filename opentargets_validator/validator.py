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

#    hash_line = DataStructureFlattener(parsed_line["unique_association_fields"]).get_hexdigest()

    hash_line = hashlib.md5(json.dumps(parsed_line["unique_association_fields"], 
        sort_keys=True).encode("utf-8")).hexdigest()

    return line_counter, validation_errors, hash_line

def validate(file_descriptor, schema_uri, loglines):
    logger = logging.getLogger(__name__)
    error_lines = abs(loglines)
    line_counter = 1
    hash_lines = dict()

    cpus = multiprocessing.cpu_count()

    stage = pypeln.process.map(validator_mapped, enumerate(file_descriptor),
        on_start=functools.partial(validate_start, schema_uri),
        workers=cpus,
        maxsize=1000)

    for line_counter, validation_errors, hash_line in stage:
        valid = True

        if validation_errors:
            valid = False
            for path, message in validation_errors:
                logger.error('fail @ %i.%s %s', line_counter, path, message)


        #check for any hash collisions
        #only check those that have passed validation so far
        if valid:
            if hash_line in hash_lines:
                valid = False
                logger.error("Duplicate hashes %d and %d ",
                    hash_lines[hash_line], line_counter)
            else:
                hash_lines[hash_line] = line_counter

        if not valid:
            #if this line had any problems, decrement the number of allowed errors
            error_lines -= 1
            if error_lines <= 0:
                #if there are too many errors, exit now
                return False

        line_counter += 1

    return valid
