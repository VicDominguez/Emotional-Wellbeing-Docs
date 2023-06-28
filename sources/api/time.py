from datetime import datetime, timedelta


def __datetime_to_millisecond_timestamp(date: datetime) -> int:
    """ Pass datetime to timestamp in milliseconds"""
    return int(date.timestamp() * 1000)


def __get_start_day(date: datetime) -> int:
    """ Get the timestamp of the start of the day"""
    return __datetime_to_millisecond_timestamp(
        date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
    )


def __get_end_day(date: datetime) -> int:
    """ Get the timestamp of the end of the day"""
    return __datetime_to_millisecond_timestamp(
        date.replace(
            hour=23,
            minute=59,
            second=59,
            microsecond=999999
        )
    )


def get_timestamps_yesterday():
    """ Get the timestamp of the start and end of yesterday"""
    yesterday = datetime.now() - timedelta(days=1)
    return __get_start_day(yesterday), __get_end_day(yesterday)


def get_timestamps_current_week():
    """Get start and end timestamp of each day of the current week"""
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)
    result = []

    day = monday
    while day <= sunday:
        result.append((__get_start_day(day), __get_end_day(day)))
        day += timedelta(days=1)

    return result


def get_timestamps_last_seven_days():
    """ Get the timestamp of the start of seven days before and the end of yesterday"""
    now = datetime.now()
    first_day = now - timedelta(days=7)
    last_day = now - timedelta(days=1)
    return __get_start_day(first_day), __get_end_day(last_day)
