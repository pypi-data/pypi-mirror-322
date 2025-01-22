from datetime import UTC, datetime


def convert_to_yyyymmdd(date_str: str) -> str:
    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%b %d, %Y",
    ]
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%Y%m%d")
        except ValueError:
            continue

    return date_str


def convert_to_hhmmss(time_str: str) -> str:
    time_formats = [
        "%H:%M:%S",
        "%H:%M:%S%:z",
        "%I:%M:%S %p",
        "%H:%M",
        "%I:%M %p",
        "%H%M%S",
    ]

    for fmt in time_formats:
        try:
            time_obj = datetime.strptime(time_str, fmt)
            return time_obj.strftime("%H%M%S")
        except ValueError:
            continue

    return time_str


def get_ymdhms() -> str:
    cur = datetime.now(UTC)
    datestr, timestr = cur.isoformat(timespec="seconds").split("T")
    return " ".join([convert_to_yyyymmdd(datestr), convert_to_hhmmss(timestr[:8])])
