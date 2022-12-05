import re
from bot.exceptions.telegram_bot_exception import TelegramBotException


class Lesson:
    __LINK_REGEX: str = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
    __TIME_REGEX: str = r"^([01][0-9])|(2[0-4])\:[0-6][0-9]$"
    __DAYS: list[str] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    __WEEKS: list[int] = [1, 2]

    def __init__(self, json: dict):
        self.__json = json
        self.name = self.__get_from_json('name')
        self.link = self.__parse_link(self.__get_from_json('link'))
        self.day = self.__parse_day(self.__get_from_json('day'))
        self.time = self.__parse_time(self.__get_from_json('time'))
        self.week = self.__parse_week(self.__get_from_json('week'))

    def __get_from_json(self, key: str):
        try:
            return self.__json.get(key)
        except KeyError:
            raise TelegramBotException("No key such as " + key)

    def get_dict(self) -> dict:
        return self.__json

    def __parse_link(self, link: str) -> str:
        match = re.match(self.__LINK_REGEX, link)
        if match is None:
            raise TelegramBotException("Link in json is incorrect")
        return link

    def __parse_day(self, day: str) -> str:
        if day not in self.__DAYS:
            raise TelegramBotException("Day in json is incorrect")
        return day

    def __parse_week(self, week: str) -> int:
        try:
            num = int(week)
        except ValueError:
            raise TelegramBotException("Week in json should be int")
        if num not in self.__WEEKS:
            raise TelegramBotException("Week in json should be either 1 or 2")
        return num

    def __parse_time(self, time: str) -> str:
        match = re.match(self.__TIME_REGEX, time)
        if match is None:
            raise TelegramBotException("Time in json is incorrect")
        return time

