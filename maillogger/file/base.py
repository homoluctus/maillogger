import gzip
from dataclasses import dataclass, field
from typing import IO, Any, Optional


@dataclass
class FileHandler:
    filepath: str
    mode: str = 'r'
    encoding: str = 'utf-8'
    newline: Optional[str] = None
    compress: bool = False
    compress_level: int = 9

    fd: Optional[IO[Any]] = field(init=False, default=None)

    def _open(self) -> IO[Any]:
        if self.fd is not None:
            return self.fd

        if self.compress:
            return gzip.open(
                self.filepath, mode=self.mode, newline=self.newline,
                encoding=self.encoding, compresslevel=self.compress_level)

        return open(
            self.filepath, mode=self.mode, newline=self.newline,
            encoding=self.encoding)

    def close(self) -> None:
        if self.fd is None:
            return

        self.fd.close()
        self.fd = None
