import json

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot.constants.database import CHAT_ID, SCHEDULE, MODULE_IS_ON
from bot.constants.emoji import CLOCK_EMOJI
from bot.constants.general import END_LINE, WHITESPACE
from bot.constants.schedule import INTERVAL_SECS_SCHEDULE
from bot.database.lesson.lesson_parser import parse_lessons_from_schedule_json
from bot.database.lesson.lesson_retriever import retrieve_lessons_from_schedule_json
from bot.database.schedule_session import ScheduleSession
from bot.database.lesson.lesson import Lesson
from bot.decorators.on_message import on_message
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.datetime_helper import get_current_week_number, get_current_time_str, \
    get_current_day_str
from bot.helpers.json_helper import check_document_is_json, load_schedule_json_from_file, create_tmp_json_filepath, \
    create_tmp_json_file, delete_tmp_files
from bot.helpers.scheduler_helper import register_connection_switchers, create_keyboard_markup, get_turn_str
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class ScheduleModule(ScheduledClient):
    scheduler: AsyncIOScheduler

    def __send_on_schedule(self, *args: int | list[Lesson]):
        lessons: list[Lesson] = args[0]
        chat_id = args[1]
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()

        for lesson in lessons:
            do_this_week: bool = (lesson.get_week() == 0) or (lesson.get_week() == week_num)
            do_this_day: bool = lesson.get_day() == day_str
            do_this_time: bool = lesson.get_time() == time_str
            if do_this_week and do_this_day and do_this_time:
                message = self.send_message(chat_id=chat_id,
                                            text=CLOCK_EMOJI + WHITESPACE + lesson.get_name() + END_LINE + lesson.get_link())
                # Delete job and
                print(message)

    def __add_previous_sessions_to_scheduler(self, schedule_session: ScheduleSession) -> AsyncIOScheduler:
        for session in schedule_session.get_all_sessions():
            chat_id = int(session.get(CHAT_ID))
            module_is_on = bool(session.get(MODULE_IS_ON))
            lessons: list[Lesson] = retrieve_lessons_from_schedule_json(session.get(SCHEDULE))  # it retrieve lessons
            job: Job = self.add_job_to_scheduler(chat_id, INTERVAL_SECS_SCHEDULE,
                                                 self.__send_on_schedule,
                                                 SCHEDULE, lessons)
            if not module_is_on:
                job.pause()
        return self.scheduler

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        self.__schedule_sessions: ScheduleSession = ScheduleSession()
        self.__add_previous_sessions_to_scheduler(self.__schedule_sessions)
        register_connection_switchers(self, SCHEDULE, self.__schedule_sessions)

        @on_message(self, filters.command(SCHEDULE) & filters.document)
        async def set_schedule(_, message: Message):
            check_document_is_json(message.document)
            filepath: str = await self.download_media(message,
                                                      file_name=create_tmp_json_filepath(SCHEDULE, message.chat.id))
            schedule: list[dict] = load_schedule_json_from_file(filepath)
            delete_tmp_files(filepath)
            lessons: list[Lesson] = parse_lessons_from_schedule_json(schedule)  # it checks and gets lessons
            self.__schedule_sessions.upsert_session(chat_id=message.chat.id, schedule=schedule)
            self.add_job_to_scheduler(message.chat.id, INTERVAL_SECS_SCHEDULE,
                                      self.__send_on_schedule,
                                      SCHEDULE, lessons)
            await self.send_success_reply_message(message, "Модуль розкладів успішно встановлено!",
                                                  create_keyboard_markup(SCHEDULE, "викл"))

        @on_message(self, filters.command(SCHEDULE))
        async def send_schedule_file(_, message: Message):
            schedule, module_is_on = self.__schedule_sessions.get_session_and_module_is_on_by_chat_id(message.chat.id)
            if schedule is None:
                await self.send_reply_document(message, "schedule.example.json")
                raise TelegramBotError("Ви ще не встановили розклад. Зверху приклад файлу.\n"
                                       "Аби встановити розклад використайте наступну команду і JSON файл:\n"
                                       "/schedule [schedule.json]")
            filepath: str = create_tmp_json_file("my_schedule", message.chat.id,
                                                 json.dumps({SCHEDULE: schedule}))
            await self.send_reply_document(message, filepath,
                                           create_keyboard_markup(SCHEDULE, get_turn_str(not module_is_on)))
            delete_tmp_files(filepath)
