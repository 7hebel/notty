""" This module is made for easy date and time handling. """

from datetime import datetime as Datetime


def generate_timestamp() -> int:
    """ Generate timestamp from current moment and
    remove milliseconds information by converting
    value to int as the ms are stored in floating
    point value. """
    return int(Datetime.now().timestamp())

def read_timestamp(timestamp: int) -> Datetime:
    """ Turn saved timestamp back to Datetime object. """
    return Datetime.fromtimestamp(timestamp)
