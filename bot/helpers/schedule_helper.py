from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters

from bot import database
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.job_helper import check_job_state
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


def add_job_to_scheduler(scheduler: AsyncIOScheduler, chat_id: int, seconds: int, send_on_schedule: (),
                         module_name: str, *args) -> Job:
    return scheduler.add_job(send_on_schedule,
                             "interval",
                             seconds=seconds,
                             id=get_unique_job_id(chat_id, module_name),
                             replace_existing=True,
                             args=[chat_id, args[0]])


def get_unique_job_id(chat_id: int, module_name: str) -> str:
    return module_name + "_job_" + chat_id.__str__()


def register_connection_switchers(client: ScheduledClient, module_name: str):
    __switch_connection(client, module_name, True)
    __switch_connection(client, module_name, False)


def __switch_connection(client: ScheduledClient, module_name: str, turn_on: bool):
    turn_on_or_off: str = ("on" if turn_on else "off")

    @on_typed_message(client, filters.command(turn_on_or_off + "_" + module_name))
    async def func(_, message):
        job: Job | None = client.scheduler.get_job(get_unique_job_id(message.chat.id, module_name))
        check_job_state(job, module_name, must_job_run=not turn_on)
        job.pause()
        database.update_gmail_module(message.chat.id, module_is_on=turn_on)
        text: str = module_name + " module is " + turn_on_or_off
        await client.send_reply_message(message, text)
