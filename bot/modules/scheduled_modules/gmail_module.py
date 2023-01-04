from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import database
from bot.constants.database import CHAT_ID, APP_PASSWORD, GMAIL_ADDRESS, MODULE_IS_ON
from bot.constants.gmail import GMAIL, INTERVAL_SECS_GMAIL
from bot.constants.help_alerts import TURN_TITLE
from bot.database import get_gmail_address_by_chat_id
from bot.decorators.on_typed_message import on_typed_message
from bot.email.gmail_client import GmailClient
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters
from bot.helpers.scheduler_helper import register_connection_switchers
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class GmailModule(ScheduledClient):

    def __send_on_schedule(self, *args: int | GmailClient):
        gmail_client: GmailClient = args[0]
        chat_id = args[1]
        texts: list[str] = gmail_client.get_new_messages()
        for text in texts:
            self.send_message(chat_id=chat_id, text=text)

    def __add_previous_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_gmail_sessions():
            chat_id = int(session.get(CHAT_ID))
            app_password = session.get(APP_PASSWORD)
            gmail_address = session.get(GMAIL_ADDRESS)
            module_is_on = bool(session.get(MODULE_IS_ON))
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            job: Job = self.add_job_to_scheduler(chat_id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                                 GMAIL, gmail_client)
            if not module_is_on:
                job.pause()
        return self.scheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        self.reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("on", callback_data=TURN_TITLE + GMAIL + "on"),
                    InlineKeyboardButton("off", callback_data=TURN_TITLE + GMAIL + "off")
                ]
            ]
        )
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__add_previous_sessions_to_scheduler()
        register_connection_switchers(self, GMAIL)

        @on_typed_message(self, filters.regex(GMAIL + r"\s*" + r"$"))
        async def send_my_gmail(_, message: Message):
            gmail_address: str = get_gmail_address_by_chat_id(message.chat.id)
            if gmail_address is None:
                raise TelegramBotException("You have not set a gmail connection yet.\n"
                                           "To set a connection, use the command with gmail app password:\n"
                                           "/gmail [gmail] [app-pass]"
                                           )
            await self.send_reply_message(message,
                                          "Your current gmail address is " + gmail_address,
                                          self.reply_markup)

        @on_typed_message(self, filters.command(GMAIL))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            database.upsert_gmail(message.chat.id, gmail_address, app_password)
            self.add_job_to_scheduler(message.chat.id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                      GMAIL, gmail_client)
            await self.send_success_reply_message(message,
                                                  "Email auth is set successfully! You may delete the message")
