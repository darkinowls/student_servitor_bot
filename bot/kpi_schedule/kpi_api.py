import json
import re
from uuid import UUID

import requests
from requests import Response

from bot.constants.regex import GROUP_REGEX
from bot.core.singleton_meta import SingletonMeta
from bot.database.lesson.lesson import Lesson
from bot.kpi_schedule.models.group import Group
from bot.kpi_schedule.models.kpi_schedule import KpiSchedule


class KpiRepo(metaclass=SingletonMeta):
    __url = "https://schedule.kpi.ua/api"

    def downloadGroups(self) -> list[Group]:
        response: Response = requests.get(self.__url + '/schedule/groups')

        groups: list[Group] = []
        for item in response.json()['data']:
            group = Group.from_dict(item)
            groups.append(group)

        cafedra = list(
            group for group in groups if group.faculty == '' and re.match(GROUP_REGEX, group.name))

        sorted_cafedra = sorted(cafedra, key=lambda x: x.name)

        with open('kpi_groups.json', mode="w", encoding='utf-8') as json_file:
            json.dump([group.__dict__ for group in sorted_cafedra], json_file, ensure_ascii=False, indent=4)

        return sorted_cafedra

    def getGroups(self) -> list[Group]:
        with open('kpi_groups.json', mode="r", encoding='utf-8') as json_file:
            json_dict = json.load(json_file)

        groups = []
        for item in json_dict:
            group = Group.from_dict(item)
            groups.append(group)

        return groups

    def getIdByGroupName(self, group_name:str) -> str:
        groups = self.getGroups()
        for group in groups:
            if group.name == group_name:
                return group.id

    def getScheduleById(self, group_id: str) -> list[dict]:
        response: Response = requests.get(self.__url + '/schedule/lessons?groupId=' + group_id)
        kpi_schedule: KpiSchedule = KpiSchedule.from_dict(response.json()['data'])
        return kpi_schedule.to_lesson_list()
