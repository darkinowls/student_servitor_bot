from abc import abstractmethod

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.constants.general import FILE_GARBAGE_COLLECTOR, INTERVAL_SECS_GARBAGE_COLLECTOR
from bot.helpers.scheduler_helper import add_job_to_scheduler
from bot.helpers.tmp_helper import delete_old_tmp_files
from bot.modules.simple_client import SimpleClient


class ScheduledClient(SimpleClient):
    scheduler: AsyncIOScheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.scheduler = AsyncIOScheduler()
        add_job_to_scheduler(self.scheduler,
                             0,
                             INTERVAL_SECS_GARBAGE_COLLECTOR,
                             delete_old_tmp_files,
                             FILE_GARBAGE_COLLECTOR,
                             INTERVAL_SECS_GARBAGE_COLLECTOR)

        self.scheduler.start()
