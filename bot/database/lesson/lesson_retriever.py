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
    name: str = get_from_json(NAME, lesson_json)
    day: str = get_from_json(DAY, lesson_json)
    time: str = get_from_json(TIME, lesson_json)
    week: int = get_from_json(WEEK, lesson_json)
    link: str = get_from_json(LINK, lesson_json)
    return Lesson(name, day, time, week, link)
