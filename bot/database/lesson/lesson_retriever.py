from bot.constants.lesson import NAME, DAY, TIME, WEEK, LINK
from bot.database.lesson.lesson import Lesson
from bot.helpers.json_helper import get_from_json


def retrieve_lessons_from_schedule_json(schedule: list[dict]) -> list[Lesson]:
    """
        It parses schedule into lessons.
        There is NO validity checks.
        The function is design for data retrieval.
        :param schedule:
        :return: list of parsed lessons
    """
    return [__retrieve_lesson(lesson_json) for lesson_json in schedule]


def __retrieve_lesson(lesson_json: dict) -> Lesson:
    name: str = lesson_json.get(NAME)
    day: str = lesson_json.get(DAY)
    time: str = lesson_json.get(TIME)
    week: int | None = lesson_json.get(WEEK)
    link: str | None = lesson_json.get(LINK)
    return Lesson(name, day, time, week, link)
