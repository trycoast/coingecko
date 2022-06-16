import datetime


def from_iso_8601(date: str) -> str:
    """ Converts an ISO 8601 date string into MM-DD-YYYY format.

    Args:
        date (str): The date in ISO 8601 format.

    Returns:
        date (str): Date in MM-DD-YYYY format
    """
    date = datetime.datetime.fromisoformat(date)
    return f'{str(date.day).zfill(2)}-{str(date.month).zfill(2)}-{date.year}'  # zfill adds a leading 0 when needed.
