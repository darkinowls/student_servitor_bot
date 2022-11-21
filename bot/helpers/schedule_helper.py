import datetime
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.lesson_helper import parse_json_to_lesson


# {
# schedule :[
# {
# lesson : "math or idk",
# link : "https//:zoom.com",
# day : "Monday",
# time : "08:30",
# week : 1,
# }
# ]
# }

def get_lessons_from_json(json: dict) -> list[dict]:
    try:
        schedule: list[dict] = json.get('schedule')
    except KeyError:
        raise TelegramBotException('No schedule object in json')
    lessons: list[dict] = []
    for json in schedule:
        lessons.append(parse_json_to_lesson(json))
    return lessons


def get_current_week_number() -> int:
    """
    :return: number of week. 1 - first week and 2 - second week
    """
    week_num: int = datetime.date.today().isocalendar().week + 1
    return 1 if week_num % 2 else 2


def get_current_time() -> tuple[int, int]:
    return datetime.datetime.today().hour, datetime.datetime.today().minute
