import datetime
from bot.database.models.lesson import Lesson
from bot.exceptions.telegram_bot_exception import TelegramBotException


def get_lessons_from_schedule_json(schedule: list[dict]) -> list[Lesson]:
    return [Lesson(lesson_json) for lesson_json in schedule]


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
