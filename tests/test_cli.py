from dataclasses import asdict, dataclass
from typing import Any, Dict

import pytest

from maillogger.cli import parse_options


@dataclass
class CliOption:
    source_file: str
    target_file: str
    fmt: str = 'csv'
    compress: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@pytest.mark.parametrize(
    'args, expectation',
    (
        (
            'maillog result',
            CliOption(source_file='maillog', target_file='result')
        ),
        (
            'maillog result -f json',
            CliOption(
                source_file='maillog',
                target_file='result',
                fmt='json')
        ),
        (
            'maillog result -f tsv',
            CliOption(
                source_file='maillog',
                target_file='result',
                fmt='tsv')
        ),
        (
            'maillog result -c',
            CliOption(
                source_file='maillog',
                target_file='result',
                compress=True)
        ),
        (
            'maillog result -c -f json',
            CliOption(
                source_file='maillog',
                target_file='result',
                fmt='json',
                compress=True)
        ),
        (
            'maillog result -c -f tsv',
            CliOption(
                source_file='maillog',
                target_file='result',
                fmt='tsv',
                compress=True)
        )
    )
)
def test_parse_options(args: str, expectation: CliOption):
    actual_result = parse_options(args=args.split())
    assert vars(actual_result) == expectation.to_dict()
