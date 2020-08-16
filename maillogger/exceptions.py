class MailloggerError(Exception):
    """Maillogger base exception class"""


class NotFoundFileError(MailloggerError):
    """Raised when a target file to load can not be found"""

    msg = 'Could not find "{filepath}"'

    def __init__(self, filepath: str) -> None:
        super().__init__(self.msg.format(filepath=filepath))


class UnsupportedDataFormatError(MailloggerError):
    """Raised when an unsupported data format is specified"""

    msg = 'Data format "{fmt}" is not supported'

    def __init__(self, fmt: str) -> None:
        super().__init__(self.msg.format(fmt=fmt))
