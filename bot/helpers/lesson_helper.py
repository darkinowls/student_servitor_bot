from bot.database.models.lesson import Lesson


def get_lessons_from_schedule_json(schedule: list[dict]) -> list[Lesson]:
    return [Lesson(lesson_json) for lesson_json in schedule]