import argparse
from argparse import RawTextHelpFormatter
import logging
import logging.config
import sys

from opentargets_urlzsource import URLZSource

from .helpers import file_or_resource
from .validator import validate
from .version import __version__


def main():
    logging.config.fileConfig(file_or_resource('logging.ini'), disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description=f'Open Targets evidence string validator, version {__version__}.', formatter_class=argparse.RawDescriptionHelpFormatter)

    input_files = parser.add_argument_group("input files", """Either of the input files listed below could be:
    * STDIN (-)
    * Local uncompressed JSON (*.json)
    * Local compressed JSON (*.json.gz)
    * Remote uncompressed JSON (https://example.com/example.json)""")
    input_files.add_argument('data_source_file', nargs='?', default='-', help='Data file to validate. If not specified, STDIN is the default.')
    input_files.add_argument("--schema", required=True, help="Schema file to validate against. Mandatory.")

    parser.add_argument("--log-level", dest='loglevel', help="Log level. Default: WARNING", default='WARNING')
    args = parser.parse_args()

    if args.loglevel:
        try:
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.getLevelName(args.loglevel))
            logger.setLevel(logging.getLevelName(args.loglevel))
        except Exception as e:
            root_logger.exception(e)

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
