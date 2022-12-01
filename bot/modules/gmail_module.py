from apscheduler.job import Job
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.decorators.on_typed_message import on_typed_message
from bot.email.gmail_client import GmailClient
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters
from bot.helpers.job_helper import check_job_state
from bot.modules.basic_bot import BasicBot


class GmailModule(BasicBot):
    __scheduler: AsyncIOScheduler

    def __send_new_email_messages(self, *args: int | GmailClient):
        chat_id = args[0]
        gmail_client: GmailClient = args[1]
        texts: list[str] = gmail_client.get_new_messages()
        for text in texts:
            self.send_message(chat_id=chat_id, text=text)

    def __add_previous_gmail_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_gmail_sessions():
            chat_id = int(session.get('chat_id'))
            app_password = session.get('app_password')
            gmail_address = session.get('gmail_address')
            module_is_on = bool(session.get('module_is_on'))
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            job: Job = self.__scheduler.add_job(self.__send_new_email_messages,
                                                "interval",
                                                seconds=10,
                                                id=self.__get_unique_gmail_job_id(chat_id),
                                                args=[chat_id, gmail_client])
            if not module_is_on:
                job.pause()
        return self.__scheduler

    def __get_unique_gmail_job_id(self, chat_id) -> str:
        return self.__scheduler.__str__() + "_gmail_job_" + chat_id.__str__()

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__scheduler = AsyncIOScheduler()
        self.__add_previous_gmail_sessions_to_scheduler().start(paused=True)

        @on_typed_message(self, filters.command("gmail"))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            gmail_client: GmailClient = GmailClient(gmail_address, app_password)
            database.upsert_gmail(message.chat.id, gmail_address, app_password)
            self.__scheduler.add_job(self.__send_new_email_messages,
                                     "interval",
                                     seconds=10,
                                     id=self.__get_unique_gmail_job_id(message.chat.id),
                                     replace_existing=True,
                                     args=[message.chat.id, gmail_client])
            await self.send_reply_message(message, "Email auth is successful! You may delete the message")

        @on_typed_message(self, filters.command("off_gmail"))
        async def off_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(self.__get_unique_gmail_job_id(message.chat.id))
            check_job_state(job, "Gmail", must_job_run=False)
            job.pause()
            database.update_gmail_module(message.chat.id, module_is_on=False)
            await self.send_reply_message(message, "Gmail module is off")

        @on_typed_message(self, filters.command("on_gmail"))
        async def on_gmail_connection(_, message: Message):
            job: Job | None = self.__scheduler.get_job(self.__get_unique_gmail_job_id(message.chat.id))
            check_job_state(job, "Gmail", must_job_run=True)
            job.resume()
            database.update_gmail_module(message.chat.id, module_is_on=True)
            await self.send_reply_message(message, "Gmail module is on")
