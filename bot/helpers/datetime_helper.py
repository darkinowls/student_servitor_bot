import datetime

from bot.constants.lesson import DAYS_MAP


def get_current_week_number() -> int:
    """
    :return: number of week. 1 - first week(odd) and 2 - second week(even)
    """
    week_num: int = datetime.date.today().isocalendar().week + 1
    return 1 if week_num % 2 else 2


def get_current_week_number_formatted() -> str:
    return "1ий" if get_current_week_number() == 1 else "2ий"


def get_current_time_str() -> str:
    return datetime.datetime.now().strftime("%H.%M")


def get_current_day_str() -> str:
    return DAYS_MAP[datetime.datetime.now().strftime("%A")]
