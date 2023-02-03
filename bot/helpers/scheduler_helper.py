from apscheduler.job import Job
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.emoji import PLAY_EMOJI, PAUSE_EMOJI
from bot.constants.general import WHITESPACE, UNDERLINE
from bot.database.session import Session
from bot.decorators.on_callback_query import on_callback_query
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


def check_job_state(job: Job, module_name: str, must_job_run: bool):
    if job is None:
        raise TelegramBotError(module_name + " is not set in this chat")
    if job.next_run_time and not must_job_run:
        raise TelegramBotError(module_name + " module is already on")
    if job.next_run_time is None and must_job_run:
        raise TelegramBotError(module_name + " module is already off")


def register_connection_switchers(client: ScheduledClient, module_name: str, session: Session):
    __register_connection_switcher(client, module_name, True, session)
    __register_connection_switcher(client, module_name, False, session)

    @on_callback_query(client, filters.regex(r"^" + module_name))
    async def switch_connection_query(_, message: Message):
        turn_str: str = message.text.split(UNDERLINE, 1)[1]
        await switch_connection(client, message, module_name, get_turn_bool(turn_str), session)
        await message.edit_reply_markup(create_keyboard_markup(module_name, reverse_turn_str(turn_str)))


def __register_connection_switcher(client: ScheduledClient, module_name: str, turn_bool: bool, session: Session):
    @on_typed_message(client, filters.command(get_turn_str(turn_bool) + "_" + module_name))
    def func(_, message):
        switch_connection(client, message, module_name, turn_bool, session)


async def switch_connection(client: ScheduledClient, message, module_name, turn_bool, session: Session):
    job: Job | None = client.scheduler.get_job(client.get_unique_job_id(message.chat.id, module_name))
    check_job_state(job, module_name, must_job_run=not turn_bool)
    session.set_session_module_is_on(message.chat.id, module_is_on=turn_bool)

    if turn_bool:
        job.resume()
        await client.send_reply_message(message, PLAY_EMOJI + WHITESPACE + module_name + " module is on")
    else:
        job.pause()
        await client.send_reply_message(message, PAUSE_EMOJI + WHITESPACE + module_name + " module is off")


def create_keyboard_markup(module_name: str, turn_str: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(turn_str + WHITESPACE + module_name,
                                     callback_data=module_name + UNDERLINE + turn_str),
            ]
        ]
    )


def reverse_turn_str(turn_str) -> str:
    return "on" if turn_str == "off" else "off"


def get_turn_str(turn_on: bool) -> str:
    return "on" if turn_on else "off"


def get_turn_bool(turn_str: str) -> bool:
    return True if turn_str == "on" else False
