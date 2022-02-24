import argparse
import logging
import logging.config
import sys

from opentargets_urlzsource import URLZSource

from .helpers import file_or_resource
from .validator import validate
from .version import __version__


def main():
    logging.config.fileConfig(file_or_resource('logging.ini'),
                              disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description=f'OpenTargets evidence string validator, version {__version__}')
    parser.add_argument('data_source_file', nargs='?', default='-',
                        help='The prefix to prepend default: STDIN')
    parser.add_argument("--schema", dest='schema',
                        help="set the schema file to use",
                        action='store')
    parser.add_argument("--log-level", dest='loglevel',
                        help="set the log level def: WARNING",
                        action='store', default='WARNING')

    args = parser.parse_args()

    if args.loglevel:
        try:
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.getLevelName(args.loglevel))
            logger.setLevel(logging.getLevelName(args.loglevel))
        except Exception as e:
            root_logger.exception(e)

    #TODO use a position argument
    if not args.schema:
        logger.error('A --schema <schemafile> has to be specified.')
        return 1

    valid = True
    if args.data_source_file == '-':
        valid = validate(sys.stdin, args.schema)
    else:
        with URLZSource(args.data_source_file).open() as fh:
            valid = validate(fh, args.schema)

    #if we had any validation errors, exit with status 2
    if not valid:
        return 2

    #if everything was fine, exit with status 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
