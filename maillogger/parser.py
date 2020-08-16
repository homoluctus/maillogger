import re
from typing import Dict, Optional


REGEX = r'(?P<month>[A-Z][a-z]{2}) (?P<day>[0-9]{,2}) ' \
    + r'(?P<time>[0-9]{2}:[0-9]{2}:[0-9]{2}) mail postfix/[a-z]+\[[0-9]+\]: ' \
    + r'(?P<id>[A-Z0-9]+): to=<(?P<to>.*@.*)>, ' \
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
            'id': '677RGS0',
            'to': 'dummy@gmail.com',
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

    return match_obj.groupdict()
