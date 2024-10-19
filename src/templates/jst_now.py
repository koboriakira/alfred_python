from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")


def jst_now() -> datetime:
    return datetime.now(JST)
