from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

from maillogger.exceptions import NotFoundFileError
from maillogger.file.base import FileHandler
from maillogger.file.filetype import is_gzip


LoadResultType = List[Any]


@dataclass
class Loader(FileHandler):
    mode: str = 'rt'

    def __post_init__(self) -> None:
        if self.exists() is False:
            raise NotFoundFileError(self.filepath)

        self.compress = is_gzip(self.filepath)

    def handle(self) -> LoadResultType:
        if self.fd is None:
            self.fd = self._open()

        result = self.load()
        self.close()

        return result

    def load(self) -> LoadResultType:
        return self.fd.read().splitlines()  # type: ignore

    def exists(self) -> bool:
        p = Path(self.filepath)
        return p.exists()
