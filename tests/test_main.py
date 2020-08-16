import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest

from maillogger.file.loader import Loader, LoadResultType
from maillogger.main import main
from tests.utils import BASE_DIR, remove_file


@pytest.mark.parametrize(
    'args, expected_target_fp',
    (
        (
            [f'{BASE_DIR}/fixtures/source/maillog', 'main1'],
            'main1.csv'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog', 'main2', '-f', 'json'],
            'main2.json'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog', 'main3', '-f', 'tsv'],
            'main3.tsv'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog', 'main4', '-c'],
            'main4.csv.gz'
        ),
        (
            [
                f'{BASE_DIR}/fixtures/source/maillog',
                'main5', '-c', '-f', 'json'
            ],
            'main5.json.gz'
        ),
        (
            [
                f'{BASE_DIR}/fixtures/source/maillog',
                'main6', '-c', '-f', 'tsv'
            ],
            'main6.tsv.gz'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog.gz', 'main7'],
            'main7.csv'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog.gz', 'main8', '-f', 'json'],
            'main8.json'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog.gz', 'main9', '-f', 'tsv'],
            'main9.tsv'
        ),
        (
            [f'{BASE_DIR}/fixtures/source/maillog.gz', 'main10', '-c'],
            'main10.csv.gz'
        ),
        (
            [
                f'{BASE_DIR}/fixtures/source/maillog.gz',
                'main11', '-c', '-f', 'json'
            ],
            'main11.json.gz'
        ),
        (
            [
                f'{BASE_DIR}/fixtures/source/maillog.gz',
                'main12', '-c', '-f', 'tsv'
            ],
            'main12.tsv.gz'
        )
    )
)
def test_main(args: List[str], expected_target_fp: str):
    sys.argv = ['maillogger'] + args
    main()

    assert Path(expected_target_fp).exists() is True

    expected_fmt = expected_target_fp.split(".")[1]
    expected_contents_fp = f'{BASE_DIR}/fixtures/correct/output.{expected_fmt}'

    if expected_fmt == 'json':
        actual_contents = JsonLoader(filepath=expected_target_fp).handle()
        expected_contents = JsonLoader(filepath=expected_contents_fp).handle()
    else:
        actual_contents = Loader(filepath=expected_target_fp).handle()
        expected_contents = Loader(filepath=expected_contents_fp).handle()

    remove_file(expected_target_fp)

    assert actual_contents == expected_contents


@dataclass
class JsonLoader(Loader):
    def load(self) -> LoadResultType:
        return json.load(self.fd)  # type: ignore
