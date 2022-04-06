import re
from dataclasses import InitVar, asdict, dataclass, field
from datetime import datetime
from typing import Dict, Optional

REGEX_PREFIX = r'(?P<month>[A-Z][a-z]{2}) +(?P<day>[0-9]{,2}) ' \
    + r'(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}) (?P<hostname>[A-Za-z0-9-]+) postfix/[a-z/]+\[[0-9]+\]: ' \
    + r'(?P<mail_id>[A-Z0-9]+): '

REGEX_FROM = REGEX_PREFIX \
    + r'from=<(?P<from_address>.*@.*)>, size=(?P<size>[0-9]+), ' \
    + r'nrcpt=(?P<nrcpt>[0-9]+) \((?P<description>.*)\)' \

REGEX_TO = REGEX_PREFIX \
    + r'to=<(?P<to_address>.*@.*)>, ' \
    + r'relay=(?P<relay>.*), delay=(?P<delay>[0-9.]+), ' \
    + r'delays=(?P<delays>[0-9][0-9/.]+), dsn=(?P<dsn>[0-9].[0-9].[0-9]), ' \
    + r'status=(?P<status>(sent|deferred|bounced)) \((?P<description>.*)\)'

PATTERN_FROM = re.compile(REGEX_FROM)
PATTERN_TO = re.compile(REGEX_TO)

ParseResultType = Dict[str, str]


def parse(target: str, parse_to: bool = True, parse_from: bool = True) -> Optional[ParseResultType]:
    """Parse postfix maillog including send status

    Args:
        target (str): maillog

    Returns:
        Optional[ParseResultType]: return one of the following dict if match

        {
            'month': 'Aug',
            'day': '1',
            'time': '10:00:00',
            'mail_id': '677RGS0',
            'to_address': 'dummy@gmail.com',
            'relay': 'local',
            'delay': '0.06',
            'delays': '0.06/0.01/0/0',
            'dsn': '2.0.0',
            'status': 'sent',
            'description': 'delivered to maildir'
        }

        {
            'month': 'Aug',
            'day': '1',
            'time': '10:00:00',
            'mail_id': '677RGS0',
            'from_address': 'dummy@gmail.com',
            'size': '12345',
            'nrcpt': '12',
            'description': 'delivered to maildir'
        }
    """

    match_from = re.search(PATTERN_FROM, target)
    match_to = re.search(PATTERN_TO, target)

    if parse_from and match_from:
        result = match_from.groupdict()
        return ParseResultFrom(**result).to_dict()
    if parse_to and match_to:
        result = match_to.groupdict()
        return ParseResultTo(**result).to_dict()

    return None


@dataclass
class ParseResult:
    month: InitVar[str]
    day: InitVar[str]
    time: InitVar[str]
    hostname: InitVar[str]

    mail_id: str
    description: str

    datetime: str = field(init=False)

    def __post_init__(self, month: str, day: str, time: str, hostname: str) -> None:
        self.datetime = self.convert2dateime(month, day, time)

    def to_dict(self) -> ParseResultType:
        return asdict(self)

    @staticmethod
    def convert2dateime(month: str, day: str, time: str) -> str:
        day = day.rjust(2, '0')
        tmp = datetime.strptime(f'{month}{day}{time}', '%b%d%H:%M:%S')
        return tmp.replace(year=datetime.now().year).strftime('%Y%m%d%H%M%S')


@dataclass
class ParseResultTo(ParseResult):
    to_address: str
    relay: str
    delay: str
    delays: str
    dsn: str
    status: str


@dataclass
class ParseResultFrom(ParseResult):
    from_address: str
    size: str
    nrcpt: str
