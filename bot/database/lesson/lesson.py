class Lesson:
    """
    lesson model
    """

    __name: str
    __day: str
    __time: str
    __week: int | None
    __link: str | None

    def __init__(self, name: str, day: str, time: str, week: int | None, link: str | None):
        self.__name = name
        self.__day = day
        self.__time = time
        self.__week = week
        self.__link = link

    def get_name(self) -> str:
        return self.__name

    def get_day(self) -> str:
        return self.__day

    def get_time(self) -> str:
        return self.__time

    def get_week(self) -> int:
        """
        0 - every week
        1 - odd week
        2 - even week
        :return:
        """
        if self.__week is None:
            return 0
        return self.__week

    def get_link(self) -> str:
        if self.__link is None:
            return "Подія розпочалась"
        return self.__link
