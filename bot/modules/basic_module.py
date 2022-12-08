from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from bot.decorators.on_message import on_message
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.command_helper import get_single_text_parameter
from bot.helpers.datetime_helper import get_current_week_number_formatted
from bot.helpers.tmp_helper import get_tmp_json_file
from bot.modules.simple_client import SimpleClient


class BasicModule(SimpleClient):

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

        @on_message(self, filters.command("json"))
        async def get_json_from_message(_, message: Message):
            """
            To get json from the message has sent
            """
            print(message)
            filepath: str = get_tmp_json_file(filename="message",
                                              chat_id=message.chat.id,
                                              text=message.__str__())
            await self.send_document(chat_id=message.chat.id, document=filepath)

        @on_message(self, filters.command("hi"))
        async def say_hello(_, message: Message):
            """
            Everyone can say hello to Bot!
            """
            await self.send_reply_message(message, bot_name + " welcomes you!")

        @on_typed_message(self, filters.reply & filters.command("copy"))
        async def set_message_text(_, message: Message):
            await self.edit_replied_message(message, text=get_single_text_parameter(message.text))

        @on_typed_message(self, filters.command("copy"))
        async def copy_message_text(_, message: Message):
            await self.send_reply_message(message, text=get_single_text_parameter(message.text))

        @on_typed_message(self, filters.command("week"))
        async def print_week_number(_, message: Message):
            await self.send_reply_message(message, text=f"Today is the {get_current_week_number_formatted()} week")

        @self.on_callback_query(filters.regex("a"))
        def a(_, callback_query: CallbackQuery):

            callback_query.answer(f"AAAAAA + {callback_query.data}")