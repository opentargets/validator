from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import str
import time
import logging
import simplejson as json
import codecs
from sys import exit
from .helpers import generate_validator_from_schema,DataStructureFlattener


def validate(file_descriptor, schema_uri, loglines):
    logger = logging.getLogger(__name__)
    error_lines = abs(loglines)
    line_counter = 1
    hash_lines = dict()

    validator = generate_validator_from_schema(schema_uri)

    for line in file_descriptor:
        valid = True
        parsed_line = None
        
        try:
            parsed_line = json.loads(line)
        except Exception as e:
            logger.error('failed parsing line %i: %s', line_counter, e)
            continue

        validation_errors = [error for error in validator.iter_errors(parsed_line)]

        if validation_errors:
            valid = False
            for validation_error in validation_errors:
                logger.error('fail @ %i.%s %s',
                    line_counter, ".".join(validation_error.absolute_path), validation_error.message)


        #check for any hash collisions
        #only check those that have passed validation so far
        if valid:
            hash_line = DataStructureFlattener(parsed_line["unique_association_fields"]).get_hexdigest()
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
