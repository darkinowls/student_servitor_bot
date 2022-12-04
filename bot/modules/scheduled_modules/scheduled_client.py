from abc import abstractmethod

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.job_helper import check_job_state
from bot.helpers.tmp_helper import delete_old_tmp_files
from bot.modules.simple_client import SimpleClient


class ScheduledClient(SimpleClient):
    _module_name: str
    _scheduler: AsyncIOScheduler

    def __add_file_garbage_collector_job(self, minutes) -> Job:
        return self._scheduler.add_job(
            delete_old_tmp_files,
            "interval",
            minutes=minutes,
            id="file_garbage_collector",
            args=[minutes]
        )

    @abstractmethod
    def _add_previous_sessions_to_scheduler(self):
        pass

    @abstractmethod
    def _send_on_schedule(self, *args):
        pass

    def _add_job(self, chat_id: int, seconds: int, *args) -> Job:
        return self._scheduler.add_job(self._send_on_schedule,
                                       "interval",
                                       seconds=seconds,
                                       id=self._get_unique_job_id(chat_id),
                                       replace_existing=True,
                                       args=[chat_id, args[0]])

    def _get_unique_job_id(self, chat_id: int):
        return self._module_name + "_job_" + chat_id.__str__()

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self._scheduler = AsyncIOScheduler()
        self.__add_file_garbage_collector_job(minutes=60)
        self._add_previous_sessions_to_scheduler()
        self._scheduler.start()

        @on_typed_message(self, filters.command("off_" + self._module_name))
        async def off_connection(_, message: Message):
            job: Job | None = self._scheduler.get_job(self._get_unique_job_id(message.chat.id))
            check_job_state(job, self._module_name, must_job_run=True)
            job.pause()
            database.update_gmail_module(message.chat.id, module_is_on=False)
            await self.send_reply_message(message, self._module_name + " module is off")

        @on_typed_message(self, filters.command("on_" + self._module_name))
        async def on_connection(_, message: Message):
            job: Job | None = self._scheduler.get_job(self._get_unique_job_id(message.chat.id))
            check_job_state(job, self._module_name, must_job_run=False)
            job.resume()
            database.update_gmail_module(message.chat.id, module_is_on=True)
            await self.send_reply_message(message, self._module_name + " module is on")
