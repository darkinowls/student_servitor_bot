import json
from abc import ABC

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.constants.database import CHAT_ID, SCHEDULE, MODULE_IS_ON
from bot.constants.general import END_LINE
from bot.database import get_schedule_by_chat_id
from bot.database.models.lesson import Lesson
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.json_helper import check_document_is_json, load_schedule_json_from_file, get_lessons_from_schedule_json
from bot.helpers.datetime_helper import get_current_week_number, get_current_time_str, \
    get_current_day_str
from bot.helpers.schedule_helper import add_job_to_scheduler, register_connection_switchers
from bot.helpers.tmp_helper import create_tmp_json_filepath, create_tmp_json_file
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class ScheduleModule(ScheduledClient):
    scheduler: AsyncIOScheduler

    def __send_on_schedule(self, *args: int | list[Lesson]):
        chat_id = args[0]
        lessons: list[Lesson] = args[1]
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()
        for lesson in lessons:
            if lesson.week == week_num and lesson.day == day_str and lesson.time == time_str:
                self.send_message(chat_id=chat_id, text=lesson.name + END_LINE + lesson.link)

    def __add_previous_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_schedule_sessions():
            chat_id = int(session.get(CHAT_ID))
            module_is_on = bool(session.get(MODULE_IS_ON))
            lessons: list[Lesson] = get_lessons_from_schedule_json(
                session.get(SCHEDULE))  # it checks and gets lessons
            job: Job = add_job_to_scheduler(self.scheduler, chat_id, self.__INTERVAL_SECS,
                                            self.__send_on_schedule,
                                            SCHEDULE, lessons)
            if not module_is_on:
                job.pause()
        return self.scheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__INTERVAL_SECS = 60
        self.__add_previous_sessions_to_scheduler()
        register_connection_switchers(self, SCHEDULE)

        @on_typed_message(self, filters.command(SCHEDULE))
        async def set_gmail_connection(_, message: Message):
            check_document_is_json(message.document)
            filepath: str = await self.download_media(message,
                                                      file_name=create_tmp_json_filepath(SCHEDULE, message.chat.id))
            schedule: list[dict] = load_schedule_json_from_file(filepath)
            lessons: list[Lesson] = get_lessons_from_schedule_json(schedule)  # it checks and gets lessons
            database.upsert_schedule(chat_id=message.chat.id, schedule=schedule)
            add_job_to_scheduler(self.scheduler, message.chat.id, self.__INTERVAL_SECS,
                                 self.__send_on_schedule,
                                 SCHEDULE, lessons)
            await self.send_success_reply_message(message, "Schedule module is successfully set!")

        @on_typed_message(self, filters.command("my_schedule"))
        async def send_schedule_file(_, message: Message):
            schedule = get_schedule_by_chat_id(message.chat.id)
            if schedule is None:
                await self.send_reply_document(message, "schedule.example.json")
                raise TelegramBotException("You have not set a schedule yet. Here is an example above.")
            filepath: str = create_tmp_json_file("my_schedule", message.chat.id, json.dumps(schedule))
            await self.send_reply_document(message, filepath)
