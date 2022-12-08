from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters

from bot import database
from bot.constants.general import INTERVAL
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


def check_job_state(job: Job, module_name: str, must_job_run: bool):
    if job is None:
        raise TelegramBotException(module_name + " is not set in this chat")
    if job.next_run_time and not must_job_run:
        raise TelegramBotException(module_name + " module is already on")
    if job.next_run_time is None and must_job_run:
        raise TelegramBotException(module_name + " module is already off")


def register_connection_switchers(client: ScheduledClient, module_name: str):
    __switch_connection(client, module_name, True)
    __switch_connection(client, module_name, False)


def __switch_connection(client: ScheduledClient, module_name: str, turn_on: bool):
    turn_on_or_off: str = "on" if turn_on else "off"

    @on_typed_message(client, filters.command(turn_on_or_off + "_" + module_name))
    async def func(_, message):
        job: Job | None = client.scheduler.get_job(client.get_unique_job_id(message.chat.id, module_name))
        check_job_state(job, module_name, must_job_run=not turn_on)
        job.pause()
        database.update_gmail_module(message.chat.id, module_is_on=turn_on)
        await client.send_success_reply_message(message, module_name + " module is " + turn_on_or_off)
