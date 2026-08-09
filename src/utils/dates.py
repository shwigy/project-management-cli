"""Small helper for validating due-date strings."""

from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"


def parse_due_date(value):
    """Validate a YYYY-MM-DD date string, returning it unchanged if valid.

    Raises ValueError with a friendly message on bad input.
    """
    if not value:
        return None
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        raise ValueError(f"due date must be in {DATE_FORMAT} format, got {value!r}")
    return value
