import re
from dataclasses import InitVar, asdict, dataclass, field
from datetime import datetime
from typing import Dict, Optional


REGEX = r'(?P<month>[A-Z][a-z]{2}) (?P<day>[0-9]{,2}) ' \
    + r'(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}) mail postfix/[a-z]+\[[0-9]+\]: ' \
    + r'(?P<mail_id>[A-Z0-9]+): to=<(?P<to_address>.*@.*)>, ' \
    + r'relay=(?P<relay>.*), delay=(?P<delay>[0-9.]+), ' \
    + r'delays=(?P<delays>[0-9][0-9/.]+), dsn=(?P<dsn>[0-9].[0-9].[0-9]), ' \
    + r'status=(?P<status>(sent|deferred|bounced)) \((?P<description>.*)\)'
PATTERN = re.compile(REGEX)

ParseResultType = Dict[str, str]


def parse(target: str) -> Optional[ParseResultType]:
    """Parse postfix maillog including send status

    Args:
        target (str): maillog

    Returns:
        Optional[ParseResultType]: return the following dict if match

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
    """

    match_obj = re.search(PATTERN, target)

    if match_obj is None:
        return None

    result = match_obj.groupdict()
    return ParseResult(**result).to_dict()


@dataclass
class ParseResult:
    month: InitVar[str]
    day: InitVar[str]
    time: InitVar[str]

    mail_id: str
    to_address: str
    relay: str
    delay: str
    delays: str
    dsn: str
    status: str
    description: str

    datetime: str = field(init=False)

    def __post_init__(self, month: str, day: str, time: str) -> None:
        self.datetime = self.convert2dateime(month, day, time)

    def to_dict(self) -> ParseResultType:
        return asdict(self)

    @staticmethod
    def convert2dateime(month: str, day: str, time: str) -> str:
        tmp = datetime.strptime(f'{month}{day}{time}', '%b%d%H:%M:%S')
        return tmp.replace(year=datetime.now().year).strftime('%Y%m%d%H%M%S')
