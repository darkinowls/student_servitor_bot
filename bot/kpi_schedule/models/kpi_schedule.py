from dataclasses import dataclass
from typing import Any
from typing import List

from bot.database.lesson.lesson import Lesson


@dataclass
class Pair:
    teacherName: str
    lecturerId: str
    type: str
    time: str
    name: str
    place: str
    tag: str

    @staticmethod
    def from_dict(obj: Any) -> 'Pair':
        _teacherName = str(obj.get("teacherName"))
        _lecturerId = str(obj.get("lecturerId"))
        _type = str(obj.get("type"))
        _time = str(obj.get("time"))
        _name = str(obj.get("name"))
        _place = str(obj.get("place"))
        _tag = str(obj.get("tag"))
        return Pair(_teacherName, _lecturerId, _type, _time, _name, _place, _tag)


@dataclass
class ScheduleFirstWeek:
    day: str
    pairs: List[Pair]

    @staticmethod
    def from_dict(obj: Any) -> 'ScheduleFirstWeek':
        _day = str(obj.get("day"))
        _pairs = [Pair.from_dict(y) for y in obj.get("pairs")]
        return ScheduleFirstWeek(_day, _pairs)


@dataclass
class ScheduleSecondWeek:
    day: str
    pairs: List[Pair]

    @staticmethod
    def from_dict(obj: Any) -> 'ScheduleSecondWeek':
        _day = str(obj.get("day"))
        _pairs = [Pair.from_dict(y) for y in obj.get("pairs")]
        return ScheduleSecondWeek(_day, _pairs)


@dataclass
class KpiSchedule:
    scheduleFirstWeek: List[ScheduleFirstWeek]
    scheduleSecondWeek: List[ScheduleSecondWeek]

    @staticmethod
    def from_dict(obj: Any) -> 'KpiSchedule':
        _scheduleFirstWeek = [ScheduleFirstWeek.from_dict(y) for y in obj.get("scheduleFirstWeek")]
        _scheduleSecondWeek = [ScheduleSecondWeek.from_dict(y) for y in obj.get("scheduleSecondWeek")]
        return KpiSchedule(_scheduleFirstWeek, _scheduleSecondWeek)

    def to_lesson_list(self) -> list[dict]:
        lesson_list = []
        for day in self.scheduleFirstWeek:
            for pair in day.pairs:
                lesson_list.append({
                    "name": pair.name,
                    "day": day.day,
                    "time": pair.time,
                    "week": 1}
                )

        for day in self.scheduleSecondWeek:
            for pair in day.pairs:
                lesson_list.append({
                    "name": pair.name,
                    "day": day.day,
                    "time": pair.time,
                    "week": 2}
                )

        return lesson_list
