import datetime


def get_current_week_number() -> int:
    """
    :return: number of week. 1 - first week and 2 - second week
    """
    week_num: int = datetime.date.today().isocalendar().week + 1
    return 1 if week_num % 2 else 2


def get_current_week_number_formatted() -> str:
    return "1st" if get_current_week_number() == 1 else "2nd"


def get_current_time_str() -> str:
    return datetime.datetime.now().strftime("%H:%M")


def get_current_day_str() -> str:
    return datetime.datetime.now().strftime("%A")
