from bot.constants.general import INTERVAL_SECS_GARBAGE_COLLECTOR, FILE_GARBAGE_COLLECTOR
from bot.helpers.json_helper import delete_old_tmp_files
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class GarbageModule(ScheduledClient):

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        self.add_job_to_scheduler(0,
                                  INTERVAL_SECS_GARBAGE_COLLECTOR,
                                  delete_old_tmp_files,
                                  FILE_GARBAGE_COLLECTOR,
                                  INTERVAL_SECS_GARBAGE_COLLECTOR)
