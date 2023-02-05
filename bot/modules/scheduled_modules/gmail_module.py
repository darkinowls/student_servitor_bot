from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot.constants.database import CHAT_ID, APP_PASSWORD, GMAIL_ADDRESS, MODULE_IS_ON
from bot.constants.gmail import GMAIL, INTERVAL_SECS_GMAIL
from bot.database.gmail_session import GmailSession
from bot.decorators.on_message import on_message

from bot.decorators.on_typed_message import on_typed_message
from bot.email.gmail_client import GmailClient
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters
from bot.helpers.scheduler_helper import register_connection_switchers, create_keyboard_markup, get_turn_str
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class GmailModule(ScheduledClient):

    def __send_on_schedule(self, *args: int | GmailClient):
        gmail_client: GmailClient = args[0]
        chat_id = args[1]
        try:
            texts: list[str] = gmail_client.get_new_messages()
            for text in texts:
                self.send_message(chat_id=chat_id, text=text)
        except TelegramBotError as error:
            self.send_message(chat_id, error.__str__())

    def __add_previous_sessions_to_scheduler(self, gmail_session: GmailSession) -> AsyncIOScheduler:

        for session in gmail_session.get_all_sessions():
            chat_id = int(session.get(CHAT_ID))
            app_password = session.get(APP_PASSWORD)
            gmail_address = session.get(GMAIL_ADDRESS)
            module_is_on = bool(session.get(MODULE_IS_ON))
            try:
                gmail_client: GmailClient = GmailClient(gmail_address, app_password)
                job: Job = self.add_job_to_scheduler(chat_id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                                     GMAIL, gmail_client)
                if not module_is_on:
                    job.pause()
            except TelegramBotError as error:
                self.send_message(chat_id, error.__str__())
        return self.scheduler

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        self.__gmail_sessions: GmailSession = GmailSession()
        self.__add_previous_sessions_to_scheduler(self.__gmail_sessions)
        register_connection_switchers(self, GMAIL, self.__gmail_sessions)

        @on_typed_message(self, filters.regex("^/" + GMAIL + r"\s.*"))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            self.__gmail_sessions.upsert_session(message.chat.id, [gmail_address, app_password])
            self.add_job_to_scheduler(message.chat.id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                      GMAIL, gmail_client)
            await self.send_success_reply_message(message,
                                                  "Email auth is set successfully! You may delete the message",
                                                  create_keyboard_markup(GMAIL, "off"))

        @on_typed_message(self, filters.command(GMAIL))
        async def send_my_gmail(_, message: Message):
            gmail_address_str, module_is_on = self.__gmail_sessions.get_session_and_module_is_on_by_chat_id(
                message.chat.id)
            if gmail_address_str is None:
                raise TelegramBotError("You have not set a gmail connection yet.\n"
                                       "To set a connection, use the command with gmail app password:\n"
                                       "/gmail [gmail] [app-pass]"
                                       )
            await self.send_reply_message(message,
                                          "Your current gmail address is " + gmail_address_str,
                                          create_keyboard_markup(GMAIL, get_turn_str(not module_is_on)))
