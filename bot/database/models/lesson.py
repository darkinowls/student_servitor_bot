import re

from bot.constants.regex import LINK_REGEX, TIME_REGEX
from bot.constants.schedule import DAYS, WEEKS, NAME, DAY, TIME, WEEK, LINK
from bot.exceptions.telegram_bot_exception import TelegramBotException


class Lesson:

    def __init__(self, json: dict):
        self.__json = json
        self.name = self.__get_from_json(NAME)
        self.day = self.__parse_day(self.__get_from_json(DAY))
        self.time = self.__parse_time(self.__get_from_json(TIME))
        self.week = self.__parse_week(self.__get_from_json(WEEK))
        if LINK in self.__json.keys():
            self.link = self.__parse_link(self.__get_from_json(LINK))
        self.link = 'The lesson has begun'

    def __get_from_json(self, key: str):
        try:
            return self.__json.get(key)
        except KeyError:
            raise TelegramBotException("No key such as " + key)

    def get_dict(self) -> dict:
        return self.__json

    @staticmethod
    def __parse_link(link: str) -> str:
        match = re.match(LINK_REGEX, link)
        if match is None:
            raise TelegramBotException("Link in json is incorrect")
        return link

    @staticmethod
    def __parse_day(day: str) -> str:
        if day not in DAYS:
            raise TelegramBotException("Day in json is incorrect")
        return day

    @staticmethod
    def __parse_week(week: str) -> int:
        try:
            num = int(week)
        except ValueError:
            raise TelegramBotException("Week in json should be int")
        if num not in WEEKS:
            raise TelegramBotException("Week in json should be either 1 or 2")
        return num

    @staticmethod
    def __parse_time(time: str) -> str:
        match = re.match(TIME_REGEX, time)
        if match is None:
            raise TelegramBotException("Time in json is incorrect")
        return time
