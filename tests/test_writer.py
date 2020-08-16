from typing import Type

import pytest

from maillogger.file.writer import (
    CsvWriter, FileWriter, JsonWriter, TsvWriter, get_writer
)
from tests.utils import BASE_DIR, is_same_file_contents, load_json, remove_file


@pytest.mark.parametrize(
    'fmt, expectation',
    (
        ('csv', CsvWriter),
        ('json', JsonWriter),
        ('tsv', TsvWriter)
    )
)
def test_get_writer(fmt: str, expectation: Type[FileWriter]):
    writer = get_writer('dummy', fmt)
    assert isinstance(writer, expectation)


@pytest.mark.parametrize(
    'writer, fmt, answer_filename',
    (
        (CsvWriter, 'csv', 'output.csv'),
        (JsonWriter, 'json', 'output.json'),
        (TsvWriter, 'tsv', 'output.tsv')
    )
)
def test_writer(writer: Type[FileWriter], fmt: str, answer_filename: str):
    output_filename_for_test = 'dummy'
    records = load_json('source/records.json')
    obj = writer(filepath=output_filename_for_test)
    obj.handle(records)

    expected_filepath = f'{output_filename_for_test}.{fmt}'
    assert obj.filepath == expected_filepath

    is_same = is_same_file_contents(
        obj.filepath, f'{BASE_DIR}/fixtures/correct/{answer_filename}')
    remove_file(expected_filepath)
    assert is_same is True
