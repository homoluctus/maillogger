import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).parent


def load_json(filename: str) -> Any:
    filepath = f'{BASE_DIR}/fixtures/{filename}'
    with open(filepath, encoding='utf-8') as fd:
        return json.load(fd)


def remove_file(filepath: str) -> None:
    Path(filepath).unlink()


def is_same_file_contents(lhs: str, rhs: str) -> bool:
    """Compare file contents

    Args:
        lhs (str)
        rhs (str)

    Returns:
        bool: returns True if two file contents is same, else False
    """

    with open(lhs) as fd:
        a = fd.readlines()
    with open(rhs) as fd:
        b = fd.readlines()
    return a == b
