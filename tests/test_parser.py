from maillogger.parser import parse
from tests.utils import BASE_DIR, load_json


def test_parser():
    with open(f'{BASE_DIR}/fixtures/source/maillog') as fd:
        logs = fd.read().splitlines()
    expectation = load_json('correct/parsed_maillog.json')

    actual_results = [parse(log) for log in logs]

    assert actual_results == expectation
