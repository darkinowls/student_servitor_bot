from bot.constants.lesson import NAME, DAY, LINK, TIME, WEEK
from bot.helpers.json_helper import get_from_json


class RawLesson:
    """
    Design for parsing data from strings to Lesson types
    All the fields are str type.
    """
    __name: str
    __day: str
    __time: str
    __week: str | None # optional
    __link: str | None # optional

    def __init__(self, lesson_json):
        self.__name: str = get_from_json(NAME, lesson_json)
        self.__day: str = get_from_json(DAY, lesson_json)
        self.__time: str = get_from_json(TIME, lesson_json)

        self.__week: None | str = None
        if WEEK in lesson_json.keys():
            self.__week: str = get_from_json(WEEK, lesson_json)

        self.__link: None | str = None
        if LINK in lesson_json.keys():
            self.__link = get_from_json(LINK, lesson_json)

    def get_name(self):
        return self.__name

    def get_day(self):
        return self.__day

    def get_time(self):
        return self.__time

    def get_week(self):
        return self.__week

    def get_link(self):
        return self.__link
