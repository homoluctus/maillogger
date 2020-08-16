import csv
import json
from dataclasses import dataclass
from typing import Any, ClassVar, List, Type

from maillogger.exceptions import UnsupportedDataFormatError
from maillogger.file.base import FileHandler
from maillogger.parser import ParseResultType


@dataclass
class FileWriter(FileHandler):
    ext: ClassVar[str] = 'txt'
    gz_ext: ClassVar[str] = 'gz'

    mode: str = 'wt'

    def __post_init__(self) -> None:
        self.normalize_filepath()
        self.add_file_ext()

    def normalize_filepath(self) -> None:
        dir_delimiter = '/'
        ext_delimiter = '.'
        tmp = self.filepath.split(dir_delimiter)
        tmp[-1] = tmp[-1].split(ext_delimiter, maxsplit=1)[0]
        self.filepath = dir_delimiter.join(tmp)

    def add_file_ext(self) -> None:
        ext = self.ext
        if self.compress:
            ext = f'{self.ext}.{self.gz_ext}'
        self.filepath = f'{self.filepath}.{ext}'

    def handle(self, records: List[ParseResultType]) -> None:
        if not records:
            return

        if self.fd is None:
            self.fd = self._open()
        self.write(records)
        self.close()

    def write(self, records: List[ParseResultType]) -> None:
        raise NotImplementedError()


@dataclass
class CsvWriter(FileWriter):
    ext = 'csv'

    newline: str = ''

    def write(self, records: List[ParseResultType]) -> None:
        writer = csv.DictWriter(self.fd, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


@dataclass
class JsonWriter(FileWriter):
    ext = 'json'

    ensure_ascii: bool = False
    indent: int = 2

    def write(self, records: List[ParseResultType]) -> None:
        json.dump(
            records,
            self.fd,  # type: ignore
            ensure_ascii=self.ensure_ascii,
            indent=self.indent)


@dataclass
class TsvWriter(FileWriter):
    ext = 'tsv'

    def write(self, records: List[ParseResultType]) -> None:
        header = '\t'.join(records[0].keys())
        self.fd.write(f'{header}\n')  # type: ignore

        tmp = ['\t'.join(r.values()) for r in records]
        self.fd.write('\n'.join(tmp))  # type: ignore


WRITERS = {
    'csv': CsvWriter,
    'json': JsonWriter,
    'tsv': TsvWriter
}


def get_writer(filepath: str, fmt: str, **kwargs: Any) -> Type[FileWriter]:
    writer = WRITERS.get(fmt)
    if writer is None:
        raise UnsupportedDataFormatError(fmt)

    return writer(filepath=filepath, **kwargs)


def write(
        filepath: str,
        records: List[ParseResultType],
        fmt: str,
        **kwargs: Any) -> None:
    fmt = fmt.lower()
    writer = get_writer(filepath, fmt, **kwargs)
    writer.handle(records)  # type: ignore
