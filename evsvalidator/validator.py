import time
import logging
import json
from helpers import generate_validator_from_schema, LogAccum


def validate(file_descriptor, schema_uri, loglines):
    logger = logging.getLogger(__name__)
    error_lines = abs(loglines)
    l = LogAccum(logger,error_lines if error_lines < 1024 else 1024)
    line_counter = 1
    parsed_line = None
    
    validator = generate_validator_from_schema(schema_uri)

    for line in file_descriptor:
        try:
            parsed_line = json.loads(line)
        except Exception as e:
            l.log(logging.ERROR, 'failed parsing line %i: %s', line_counter, e)

        t1 = time.time()
        validation_errors = [str(e) for e in validator.iter_errors(parsed_line)]
        t2 = time.time()
    
        if validation_errors:
            # here I have to log all fails to logger and elastic
            error_messages = ' '.join(validation_errors).replace('\n', ' ; ').replace('\r', '')
    
            error_messages_len = len(error_messages)
    
            # capping error message to 2048
            error_messages = error_messages if error_messages_len <= 2048 \
                else error_messages[:2048] + ' ; ...'
    
            l.log(logging.ERROR, 'failed validating line %i '
                  'eval %s secs with these errors %s',
                  line_counter, str(t2 - t1), error_messages)
            
            error_lines -= 1
            if error_lines <= 0:
                l.flush(True)
                logger.warning('too many errors parsing the file, so exiting')
                return
    
        line_counter += 1
        
    l.flush(True)