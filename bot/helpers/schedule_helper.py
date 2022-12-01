import datetime
from bot.database.models.lesson import Lesson
from bot.exceptions.telegram_bot_exception import TelegramBotException


def get_lessons_from_schedule_json(json: dict) -> list[Lesson]:
    try:
        schedule: list[dict] = json.get('schedule')
    except KeyError:
        raise TelegramBotException('No schedule object in json')
    lessons: list[Lesson] = []
    for lesson_json in schedule:
        lessons.append(Lesson(lesson_json))
    return lessons


def get_current_week_number() -> int:
    """
    :return: number of week. 1 - first week and 2 - second week
    """
    week_num: int = datetime.date.today().isocalendar().week + 1
    return 1 if week_num % 2 else 2


def get_current_time_str() -> str:
    return datetime.datetime.now().strftime("%H:%M")


def get_current_day_str() -> str:
    return datetime.datetime.now().strftime("%A")