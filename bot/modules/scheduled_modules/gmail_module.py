from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.database import get_gmail_address_by_chat_id
from bot.decorators.on_typed_message import on_typed_message
from bot.email.gmail_client import GmailClient
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters
from bot.helpers.schedule_helper import register_connection_switchers, add_job_to_scheduler
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class GmailModule(ScheduledClient):

    def __send_on_schedule(self, *args: int | GmailClient):
        chat_id = args[0]
        gmail_client: GmailClient = args[1]
        texts: list[str] = gmail_client.get_new_messages()
        for text in texts:
            self.send_message(chat_id=chat_id, text=text)

    def __add_previous_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_gmail_sessions():
            chat_id = int(session.get('chat_id'))
            app_password = session.get('app_password')
            gmail_address = session.get('gmail_address')
            module_is_on = bool(session.get('module_is_on'))
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            job: Job = add_job_to_scheduler(self.scheduler, chat_id, 10, self.__send_on_schedule,
                                            self.__module_name, gmail_client)
            if not module_is_on:
                job.pause()
        return self.scheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__module_name = "gmail"
        self.__add_previous_sessions_to_scheduler()
        register_connection_switchers(self, self.__module_name)

        @on_typed_message(self, filters.command("gmail"))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            database.upsert_gmail(message.chat.id, gmail_address, app_password)
            add_job_to_scheduler(self.scheduler, message.chat.id, 10, self.__send_on_schedule,
                                 self.__module_name, gmail_client)
            await self.send_reply_message(message, "Email auth is successful! You may delete the message")

        @on_typed_message(self, filters.command("my_gmail"))
        async def send_schedule_file(_, message: Message):
            gmail_address = get_gmail_address_by_chat_id(message.chat.id)
            if gmail_address is None:
                raise TelegramBotException("You have not set a gmail connection yet")
            await self.send_reply_message(message, "Your gmail address is " + gmail_address)
