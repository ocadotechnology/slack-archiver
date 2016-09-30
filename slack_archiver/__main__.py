from __future__ import absolute_import

import configargparse
import logging
import re
import sys

from . import archiver


LOGGER = logging.getLogger(__name__)


def main(args=None):
    """The main routine."""
    parser = configargparse.ArgParser(
        auto_env_var_prefix='ARCHIVER_',
    )
    parser.add('--inactivity-days', default=30, type=int)
    parser.add('--api-token', required=True)
    parser.add('--check-interval', default=60*60, type=int)
    parser.add('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO')
    parser.add('--valid-channel-regex', default='temp-.*', type=re.compile)

    options = vars(parser.parse_args(args or sys.argv[1:]))

    logging.basicConfig(level=options.pop('log_level'))

    archiver.run(**options)

if __name__ == "__main__":
    main()
