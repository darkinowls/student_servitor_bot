import schedule
from apscheduler.job import Job
from imbox import Imbox
from pyrogram import filters
from pyrogram.types import Message

from bot import email, database
from bot.decorators.on_typed_message import on_typed_message
from bot.email.gmail_client import GmailClient
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters, check_gmail_job, \
    send_new_email_messages, add_previous_gmail_sessions_to_schedule
from bot.modules.basic_module import BasicBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class GmailBot(BasicBot):
    __scheduler: AsyncIOScheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__scheduler = AsyncIOScheduler()
        add_previous_gmail_sessions_to_schedule(self.__scheduler).start(paused=True)

        @on_typed_message(self, filters.command("gmail"))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            database.upsert_gmail(message.chat.id, gmail_address, app_password)
            self.__scheduler.add_job(send_new_email_messages,
                                     "interval",
                                     seconds=10,
                                     id=message.chat.id.__str__(),
                                     replace_existing=True,
                                     args=[message.chat.id, gmail_client])
            await self.send_text_message(message, "Email auth is successful! You may delete the message")

        @on_typed_message(self, filters.command("off_gmail"))
        async def off_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(message.chat.id.__str__())
            check_gmail_job(job)
            if job.next_run_time is None:
                TelegramBotException("Gmail module is already off")
            job.pause()
            database.update_gmail_module(message.chat.id, module_is_on=False)
            await self.send_text_message(message, "Gmail module is off")

        @on_typed_message(self, filters.command("on_gmail"))
        async def on_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(message.chat.id.__str__())
            check_gmail_job(job)
            if job.next_run_time:
                TelegramBotException("Gmail module is already on")
            job.resume()
            database.update_gmail_module(message.chat.id, module_is_on=True)
            await self.send_text_message(message, "Gmail module is on")
