class Lesson:
    """
    lesson model
    """

    __name: str
    __day: str
    __time: str
    __week: int
    __link: str

    def __init__(self, name: str, day: str, time: str, week: int, link: str):
        self.__name = name
        self.__day = day
        self.__time = time
        self.__week = week
        self.__link = link

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
