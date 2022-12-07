from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.constants.general import FILE_GARBAGE_COLLECTOR, INTERVAL_SECS_GARBAGE_COLLECTOR, INTERVAL
from bot.helpers.tmp_helper import delete_old_tmp_files
from bot.modules.simple_client import SimpleClient


class ScheduledClient(SimpleClient):
    scheduler: AsyncIOScheduler

    def __get_unique_job_id(self, chat_id: int, module_name: str) -> str:
        return module_name + "_job_" + chat_id.__str__()

    def add_job_to_scheduler(self, chat_id: int, seconds: int, function: (), module_name: str, *args) -> Job:
        return self.scheduler.add_job(function,
                                      INTERVAL,
                                      seconds=seconds,
                                      id=self.__get_unique_job_id(chat_id, module_name),
                                      replace_existing=True,
                                      args=[args[0], chat_id])

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.scheduler = AsyncIOScheduler()
        self.add_job_to_scheduler(0,
                                  INTERVAL_SECS_GARBAGE_COLLECTOR,
                                  delete_old_tmp_files,
                                  FILE_GARBAGE_COLLECTOR,
                                  INTERVAL_SECS_GARBAGE_COLLECTOR)

        self.scheduler.start()
