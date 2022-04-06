from dataclasses import asdict, dataclass, field
from typing import Dict, List

from maillogger.parser import ParseResultType, ParseResultTo

GroupedResultType = Dict[str, List[ParseResultType]]
AggregateResultType = List[Dict[str, str]]


def group_by_mail_id(results: List[ParseResultType]) -> GroupedResultType:
    """Group a list of parse results into a dict by mail_id

    Args:
        results (List[ParseResultType]): List of parse results as dicts

    Returns:
        GroupedResultType: return a dictionary with the mail_id as key

        {
            '677RGS0': [
                {...}, {...}
            ]
        }
    """

    groups = {}

    for result in results:
        groups.setdefault(result['mail_id'], []).append(result)

    return groups


def aggregate(groups: GroupedResultType) -> AggregateResultType:
    """Aggregate all results per mail id into one item

    Args:
        groups (GroupedResultType): dict of lists grouped by mail id

    Returns:
        AggregateResultType: dictionary with one dict keyed by mail id
    """

    aggregates = {}

    for mail_id, records in groups.items():
        for record in records:
            aggregates.setdefault(mail_id, AggregateResult(mail_id)).update(record)

    return [aggregate.to_dict() for aggregate in aggregates.values()]


@dataclass
class AggregateResult:
    mail_id: str

    from_address: str = ''
    to_addresses: List[str] = field(default_factory=list)

    size: str = '0'

    def to_dict(self) -> ParseResultType:
        return asdict(self)

    def update(self, record: ParseResultType) -> None:
        if not self.mail_id:
            self.mail_id = record["mail_id"]
        elif record["mail_id"] != self.mail_id:
            raise ValueError("Trying to aggregate different mail ids!")

        if "from_address" in record:
            self.from_address = record["from_address"]

        if "size" in record:
            self.size = record["size"]

        if "to_address" in record:
            self.to_addresses.append(record["to_address"])
