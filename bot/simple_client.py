from collections.abc import Callable
from typing import Coroutine

from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message

from bot.exceptions.telegram_bot_exception import TelegramBotException


class SimpleClient(Client):

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    async def send_reply_message(self, incoming_message: Message, text: str):
        return await self.send_message(chat_id=incoming_message.chat.id,
                                       reply_to_message_id=incoming_message.id,
                                       text=text)

    async def edit_text_message(self, incoming_message: Message, text: str):
        return await self.edit_message_text(chat_id=incoming_message.chat.id,
                                            message_id=incoming_message.reply_to_message_id,
                                            text=text)

    async def run_wrapped_function(self, message: Message, func: Callable):
        try:
            await func(self, message)
        except TelegramBotException as e:
            print(e)
            await self.send_reply_message(message, text=e.__str__())
