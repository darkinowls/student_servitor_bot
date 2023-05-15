import re

from bot.constants.lesson import DAYS, WEEKS
from bot.constants.regex import LINK_REGEX, TIME_REGEX
from bot.database.lesson.lesson import Lesson
from bot.database.lesson.raw_lesson import RawLesson
from bot.exceptions.telegram_bot_error import TelegramBotError


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
    week: int | None = __parse_week(raw_lesson.get_week())
    link: str | None = __parse_link(raw_lesson.get_link())
    return Lesson(name, day, time, week, link)


def __parse_name(name: str) -> str:
    if len(name) > 100:
        raise TelegramBotError('Некоректне значення ' + name[0:10] + '...' +
                               '\nЗначення поля "name" надто довге')
    return name


def __parse_link(link: str | None) -> str | None:
    if link is None:
        return None
    match = re.match(LINK_REGEX, link)
    if match is None:
        raise TelegramBotError(
            'Некоректне значення ' + link[0:10] + '...' +
            '\nЗначення поля "link" може містити тільки коректне посилання')
    return link


def __parse_day(day: str) -> str:
    if day not in DAYS:
        raise TelegramBotError('Некоректне значення ' + day +
                               '\nЗначення поля "day" має містити день тижня'
                               '\nНаприклад, "Пн"')
    return day


def __parse_week(week: str | None) -> int | None:
    if week is None:
        return None
    error_text: str = 'Некоректне значення ' + str(week) + \
                      '\nЗначення поля "week" може містити тільки число 1 або 2'
    try:
        num = int(week)
    except ValueError:
        raise TelegramBotError(error_text)
    if num not in WEEKS:
        raise TelegramBotError(error_text)
    return num


def __parse_time(time: str) -> str:
    match = re.match(TIME_REGEX, time)
    if match is None:
        raise TelegramBotError(
            'Некоректне значення ' + time +
            '\nЗначення поля "time" має бути тільки часом'
            '\nПриклад - "12.30"')
    return time
