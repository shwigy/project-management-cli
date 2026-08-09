"""Due-date parsing, backed by python-dateutil for flexible input formats."""

from dateutil import parser as dateutil_parser
from dateutil.parser import ParserError

DATE_FORMAT = "%Y-%m-%d"


def parse_due_date(value):
    """Parse a user-supplied due date (e.g. "2026-09-01", "Sept 1 2026",
    "09/01/2026") and normalize it to YYYY-MM-DD for storage.

    Raises ValueError with a friendly message on unparseable input.
    """
    if not value:
        return None
    try:
        parsed = dateutil_parser.parse(value)
    except (ParserError, ValueError, OverflowError):
        raise ValueError(f"could not parse due date: {value!r}")
    return parsed.strftime(DATE_FORMAT)
