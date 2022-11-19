import random
import string

from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.command_helper import get_parameter
from bot.helpers.tmp_helper import get_or_create_tmp_json_file
from bot.simple_client import SimpleClient


class BasicBot(SimpleClient):
    async def wrap_try_except(self, func: (), message: Message):
        """
        It wraps try-except around a function.
        Is types TelegramBotException to end-user, when the exception occurs
        :param func: function
        :param message: Message
        :return: None
        """
        try:
            await func(message)
        except TelegramBotException as e:
            print(e)
            await self.send_text_message(message, text=e.__str__())

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

        @self.on_message(filters.command("json"))
        async def get_json_from_message(_, message: Message):
            """
            To get json from the message has sent
            """
            print(message)
            filepath: str = get_or_create_tmp_json_file(filename="message",
                                                        chat_id=message.chat.id,
                                                        text=message.__str__())
            await self.send_document(chat_id=message.chat.id, document=filepath)

        @self.on_message(filters.command("hi"))
        async def say_hello(_, message: Message):
            """
            Everyone can say hello to Bot!
            """
            await self.send_text_message(message, bot_name + " welcomes you!")

        @self.on_message(filters.reply & filters.command("copy"))
        @self.on_edited_message(filters.reply & filters.command("copy"))
        async def set_message_text(_, message: Message):
            await self.edit_text_message(message, text=get_parameter(message))

        @self.on_message(filters.command("copy"))
        @self.on_edited_message(filters.command("copy"))
        async def copy_message_text(_, message: Message):
            await self.send_text_message(message, text=get_parameter(message))
