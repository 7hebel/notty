from datetime import datetime


def generate_timestamp() -> int:
    now = datetime.now()
    return int(now.timestamp())

def read_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)

