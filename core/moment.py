from datetime import datetime


def generate_timestamp() -> int:
    now = datetime.now()
    return int(now.timestamp())

def read_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)

def readable_datetime(dt: datetime) -> str:
    """ Format: dd/mm/YYYY, hh:mm:ss"""
    return dt.strftime("%d/%m/%Y, %H:%M:%S")
