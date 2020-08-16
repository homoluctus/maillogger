import argparse
from typing import List, Optional

from maillogger import __version__


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='maillogger',
        description='Analysis tool for Postfix log in /var/log/maillog'
    )
    return parser


def setup_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'source_file',
        help='Specify Postfix maillog file'
    )

    parser.add_argument(
        'target_file',
        help='''Specify the filename to write parsed maillog.
        The file extension is automatically added to the end of filename.
        '''
    )

    parser.add_argument(
        '-f', '--format',
        choices=['csv', 'tsv', 'json'],
        dest='fmt',
        default='csv',
        help='File data format to write the parsed maillog (Default: csv)'
    )

    parser.add_argument(
        '-c', '--compress',
        action='store_true',
        help='Compress the output file with gzip'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help='Show maillogger command version'
    )


def parse_options(args: Optional[List[str]] = None) -> argparse.Namespace:
    parser = get_parser()
    setup_options(parser)
    return parser.parse_args(args=args)
