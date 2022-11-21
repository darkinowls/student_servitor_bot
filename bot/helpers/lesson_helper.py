import re
from bot.exceptions.telegram_bot_exception import TelegramBotException

__LINK_REGEX: str = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
__TIME_REGEX: str = r"^([01][0-9])|(2[0-4])\:[0-6][0-9]$"
__DAYS: list[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def __get_from_json(key: str, json: dict):
    try:
        return json.get(key)
    except KeyError:
        raise TelegramBotException("No key such as " + key)


def parse_json_to_lesson(json: dict):
    lesson = dict()
    lesson['name'] = __get_from_json('name', json)
    lesson['link'] = __parse_link(__get_from_json('link', json))
    lesson['day'] = __parse_day(__get_from_json('day', json))
    lesson['time'] = __parse_time(__get_from_json('time', json))
    lesson['week'] = __parse_week(__get_from_json('week', json))
    return lesson


def __parse_link(link: str) -> str:
    match = re.match(__LINK_REGEX, link)
    if match is None:
        raise TelegramBotException("Link in json is incorrect")
    return link


def __parse_day(day: str) -> str:
    if day not in __DAYS:
        raise TelegramBotException("Day in json is incorrect")
    return day


def __parse_week(week: str) -> int:
    try:
        num = int(week)
    except ValueError:
        raise TelegramBotException("Week in json should be int")
    if num not in [1, 2]:
        raise TelegramBotException("Week in json should be either 1 or 2")
    return num


def __parse_time(time: str) -> str:
    match = re.match(__TIME_REGEX, time)
    if match is None:
        raise TelegramBotException("Time in json is incorrect")
    return time
