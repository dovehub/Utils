from datetime import datetime, timedelta


def get_today() -> datetime:
    now = datetime.now()
    today = now - timedelta(hours=now.hour,
                            minutes=now.minute,
                            seconds=now.second,
                            microseconds=now.microsecond)
    return today
