from abc import abstractmethod

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.constants.general import INTERVAL
from bot.helpers.tmp_helper import delete_old_tmp_files
from bot.modules.simple_client import SimpleClient


class ScheduledClient(SimpleClient):
    scheduler: AsyncIOScheduler
    __FILE_GARBAGE_COLLECTOR = "file_garbage_collector"

    def __add_file_garbage_collector_job(self, minutes) -> Job:
        return self.scheduler.add_job(
            delete_old_tmp_files,
            INTERVAL,
            minutes=minutes,
            id=self.__FILE_GARBAGE_COLLECTOR,
            args=[minutes]
        )

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.scheduler = AsyncIOScheduler()
        self.__add_file_garbage_collector_job(minutes=60)
        self.scheduler.start()
