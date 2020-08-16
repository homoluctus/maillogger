import pytest

from maillogger.file.filetype import is_gzip
from maillogger.file.loader import Loader
from tests.utils import BASE_DIR


@pytest.mark.parametrize(
    'filename, expectation',
    (
        ('maillog', False),
        ('maillog.gz', True)
    )
)
def test_is_gzip(filename: str, expectation: bool):
    filepath = f'{BASE_DIR}/fixtures/source/{filename}'
    actual_result = is_gzip(filepath)
    assert actual_result == expectation


@pytest.mark.parametrize(
    'filename',
    (
        ('maillog'),
        ('maillog.gz')
    )
)
def test_loader(filename: str):
    target = f'{BASE_DIR}/fixtures/source/{filename}'
    loader = Loader(filepath=target)
    actual_result = loader.handle()

    # The contents of maillog and maillog.gz are the same
    expectation_fp = f'{BASE_DIR}/fixtures/source/maillog'
    with open(expectation_fp) as fd:
        expectation = fd.read().splitlines()

    assert actual_result == expectation
