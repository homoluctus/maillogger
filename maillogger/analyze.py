from typing import Dict, List

from maillogger.parser import ParseResultType


def group_by_mail_id(results: List[ParseResultType]) -> Dict[str, List[ParseResultType]]:
    """Group a list of parse results into a dict by mail_id

    Args:
        results (List[ParseResultType]): List of parse results as dicts

    Returns:
        Dict[str, List[ParseResultType]]: return a dictionary with the mail_id as key

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
