import schedule
from apscheduler.job import Job
from imbox import Imbox
from pyrogram import filters
from pyrogram.types import Message

from bot import email, database
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.gmail_helper import get_email_address_and_app_password_from_parameters, check_gmail_job
from bot.modules.basic_module import BasicBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class GmailBot(BasicBot):
    __gmail_job: Job | None

    async def send_new_email_messages(self, *args: int | Imbox):
        chat_id = args[0]
        # imbox:Imbox = args[1]
        gmail_address, app_password = database.get_gmail_address_and_app_password_by_chat_id(chat_id)
        texts: list[str] = email.get_new_messages(gmail_address, app_password)
        for text in texts:
            await self.send_message(chat_id=chat_id, text=text)

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__gmail_job = None

        @on_typed_message(self, filters.command("gmail"))
        async def set_gmail_connection(_, message: Message):
            email_address, app_password = get_email_address_and_app_password_from_parameters(message.text)
            email.get_connection(email_address, app_password)
            await self.send_text_message(message, "Email auth is successful! You may delete the message")
            database.upsert_gmail(message.chat.id, email_address, app_password)
            self.__scheduler = AsyncIOScheduler()
            self.__gmail_job = self.__scheduler.add_job(self.send_new_email_messages,
                                                        "interval",
                                                        seconds=10,
                                                        args=[message.chat.id])
            self.__scheduler.start()

        @on_typed_message(self, filters.command("off_gmail"))
        async def off_gmail_connection(_, message: Message):
            check_gmail_job(self.__gmail_job)
            self.__gmail_job.pause()
            await self.send_text_message(message, "Gmail module is off")

        @on_typed_message(self, filters.command("on_gmail"))
        async def on_gmail_connection(_, message: Message):
            check_gmail_job(self.__gmail_job)
            self.__gmail_job.resume()
            await self.send_text_message(message, "Gmail module is on")
