from collections.abc import Callable

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.types import User
from bot.constants.emoji import CHECK_BOX_EMOJI
from bot.constants.general import WHITESPACE
from bot.exceptions.telegram_bot_exception import TelegramBotException


class SimpleClient(Client):

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    @staticmethod
    async def send_reply_message(incoming_message: Message, text: str,
                                 reply_markup: InlineKeyboardMarkup = None) -> Message:
        return await incoming_message.reply_text(text=text, quote=True, reply_markup=reply_markup)

    async def send_success_reply_message(self, incoming_message: Message, text: str) -> Message:
        return await self.send_reply_message(incoming_message, CHECK_BOX_EMOJI + WHITESPACE + text)

    @staticmethod
    async def edit_replied_message(incoming_message: Message, text: str,
                                   reply_markup: InlineKeyboardMarkup = None) -> Message:
        return await incoming_message.reply_to_message.edit_text(text, reply_markup=reply_markup)

    @staticmethod
    async def send_reply_document(incoming_message: Message, filepath: str) -> Message:
        return await incoming_message.reply_document(document=filepath, quote=True)

    async def run_wrapped_function(self, message: Message, func: Callable):
        try:
            await func(self, message)
        except TelegramBotException as exception:
            print(exception)
            await self.send_reply_message(message, text=exception.__str__())


