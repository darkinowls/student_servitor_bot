import re

from bot.constants.regex import LINK_REGEX, TIME_REGEX
from bot.constants.lesson import DAYS, WEEKS, NAME, DAY, TIME, WEEK, LINK
from bot.database.lesson.lesson import Lesson
from bot.database.lesson.raw_lesson import RawLesson
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.json_helper import get_from_json


def parse_lessons_from_schedule_json(schedule: list[dict]) -> list[Lesson]:
    """
        It parses schedule into lessons.
        There is a validity checks.
        The function is design for parsing a json file.
        :param schedule:
        :return: list of parsed lessons
    """
    return [__parse_lesson(RawLesson(lesson_json)) for lesson_json in schedule]


def __parse_lesson(raw_lesson: RawLesson) -> Lesson:
    name: str = __parse_name(raw_lesson.get_name())
    day: str = __parse_day(raw_lesson.get_day())
    time: str = __parse_time(raw_lesson.get_time())
    week: int = __parse_week(raw_lesson.get_week())
    if raw_lesson.get_link():
        link = __parse_link(raw_lesson.get_link())
    else:
        link: str = "The event has started"

    return Lesson(name, day, time, week, link)


def __parse_name(name: str) -> str:
    if len(name) > 100:
        raise TelegramBotError("Name in json has more than 100 characters")
    return name


def __parse_link(link: str) -> str:
    match = re.match(LINK_REGEX, link)
    if match is None:
        raise TelegramBotError("Link in json is incorrect")
    return link


def __parse_day(day: str) -> str:
    if day not in DAYS:
        raise TelegramBotError("Day in json is incorrect. No such a day")
    return day


def __parse_week(week: str) -> int:
    try:
        num = int(week)
    except ValueError:
        raise TelegramBotError("Week in json should be int")
    if num not in WEEKS:
        raise TelegramBotError("Week in json should be either 1 or 2")
    return num


def __parse_time(time: str) -> str:
    match = re.match(TIME_REGEX, time)
    if match is None:
        raise TelegramBotError("Time in json is in incorrect format")
    return time
