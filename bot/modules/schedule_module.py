from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.json_helper import check_document_is_json, load_json_file
from bot.helpers.schedule_helper import get_lessons_from_json
from bot.helpers.tmp_helper import generate_tmp_filepath
from bot.modules.basic_module import BasicBot


class ScheduleBot(BasicBot):
    __scheduler: AsyncIOScheduler

    # def send_new_email_messages(self, *args: int | list[Lesson]):
    #     chat_id = args[0]
    #     gmail_client: list[Lesson] = args[1]
    #     texts: list[str] = gmail_client.get_new_messages()
    #     for text in texts:
    #         self.send_message(chat_id=chat_id, text=text)
    def prints(self, *args):
        print("HELLO")

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        self.__scheduler = AsyncIOScheduler()

        # add_previous_schedule_sessions_to_schedule(self.__scheduler).start(paused=True)

        @on_typed_message(self, filters.command("schedule"))
        async def set_gmail_connection(_, message: Message):
            check_document_is_json(message.document)
            filepath: str = await self.download_media(message,
                                                      file_name=generate_tmp_filepath("schedule", message.chat.id))
            json = load_json_file(filepath)
            schedule: list[dict] = get_lessons_from_json(json)
            database.upsert_schedule(chat_id=message.chat.id, schedule=schedule)
            self.__scheduler.add_job(self.prints,
                                     "interval",
                                     seconds=1,
                                     id=message.chat.id.__str__(),
                                     replace_existing=True,
                                     args=[message.chat.id, schedule])
            self.__scheduler.start()
            await self.send_text_message(message, "Schedule is successfully set!")


        # @on_typed_message(self, filters.command("off_schedule"))
        # async def off_gmail_connection(_, message: Message):
        #     job: Job | None = self.__scheduler.get_job(message.chat.id.__str__())
        #     check_gmail_job(job)
        #     if job.next_run_time is None:
        #         TelegramBotException("Gmail module is already off")
        #     job.pause()
        #     database.update_gmail_module(message.chat.id, module_is_on=False)
        #     await self.send_text_message(message, "Gmail module is off")
        #
        # @on_typed_message(self, filters.command("on_schedule"))
        # async def on_gmail_connection(_, message: Message):
        #     job: Job | None = self.__scheduler.get_job(message.chat.id.__str__())
        #     check_gmail_job(job)
        #     if job.next_run_time:
        #         TelegramBotException("Gmail module is already on")
        #     job.resume()
        #     database.update_gmail_module(message.chat.id, module_is_on=True)
        #     await self.send_text_message(message, "Gmail module is on")
