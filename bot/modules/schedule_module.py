from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.database.models.lesson import Lesson
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.job_helper import check_job_state
from bot.helpers.json_helper import check_document_is_json, load_schedule_json_from_file
from bot.helpers.schedule_helper import get_lessons_from_schedule_json, get_current_week_number, get_current_time_str, \
    get_current_day_str
from bot.helpers.tmp_helper import generate_tmp_filepath
from bot.modules.basic_bot import BasicBot


class ScheduleModule(BasicBot):
    __scheduler: AsyncIOScheduler

    def __send_lesson_on_schedule(self, *args: int | list[Lesson]):
        chat_id = args[0]
        lessons: list[Lesson] = args[1]
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()
        for lesson in lessons:
            if lesson.week == week_num and lesson.day == day_str and lesson.time == time_str:
                self.send_message(chat_id=chat_id, text=lesson.name + '\n' + lesson.link)

    def __add_previous_schedule_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_schedule_sessions():
            chat_id = int(session.get('chat_id'))
            module_is_on = bool(session.get('module_is_on'))
            lessons: list[Lesson] = get_lessons_from_schedule_json(
                session.get('schedule'))  # it checks and gets lessons
            job: Job = self.__scheduler.add_job(self.__send_lesson_on_schedule,
                                                "interval",
                                                minutes=1,
                                                id=self.__get_unique_schedule_job_id(chat_id),
                                                args=[chat_id, lessons])
            if not module_is_on:
                job.pause()
        return self.__scheduler

    def __get_unique_schedule_job_id(self, chat_id):
        return self.__scheduler.__str__() + "_schedule_job_" + chat_id.__str__()

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__scheduler = AsyncIOScheduler()
        self.__add_previous_schedule_sessions_to_scheduler().start(paused=True)

        @on_typed_message(self, filters.command("schedule"))
        async def set_gmail_connection(_, message: Message):
            check_document_is_json(message.document)
            filepath: str = await self.download_media(message,
                                                      file_name=generate_tmp_filepath("schedule", message.chat.id))
            schedule_json = load_schedule_json_from_file(filepath)
            lessons: list[Lesson] = get_lessons_from_schedule_json(schedule_json)  # it checks and gets lessons
            database.upsert_schedule(chat_id=message.chat.id, schedule_json=schedule_json)
            self.__scheduler.add_job(self.__send_lesson_on_schedule,
                                     "interval",
                                     minutes=1,
                                     id=self.__get_unique_schedule_job_id(message.chat.id),
                                     replace_existing=True,
                                     args=[message.chat.id, lessons])
            self.__scheduler.start()
            await self.send_reply_message(message, "Schedule module is successfully set!")

        @on_typed_message(self, filters.command("off_schedule"))
        async def off_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(self.__get_unique_schedule_job_id(message.chat.id))
            check_job_state(job, "Schedule", must_job_run=False)
            job.pause()
            database.update_schedule_module(message.chat.id, module_is_on=False)
            await self.send_reply_message(message, "Schedule module is off")

        @on_typed_message(self, filters.command("on_schedule"))
        async def on_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(self.__get_unique_schedule_job_id(message.chat.id))
            check_job_state(job, "Schedule", must_job_run=True)
            job.resume()
            database.update_schedule_module(message.chat.id, module_is_on=True)
            await self.send_reply_message(message, "Schedule module is on")
