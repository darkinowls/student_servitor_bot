class Lesson:
    """
    lesson model
    """

    name: str
    day: str
    time: str
    week: int | None
    link: str | None

    def __init__(self, name: str, day: str, time: str, week: int | None, link: str | None):
        self.name = name
        self.day = day
        self.time = time
        self.week = week
        self.link = link

    def get_name(self) -> str:
        return self.name

    def get_day(self) -> str:
        return self.day

    def get_time(self) -> str:
        return self.time

    def get_week(self) -> int:
        """
        0 - every week
        1 - odd week
        2 - even week
        :return:
        """
        if self.week is None:
            return 0
        return self.week

    def get_link(self) -> str:
        if self.link is None:
            return "Подія розпочалась"
        return self.link
