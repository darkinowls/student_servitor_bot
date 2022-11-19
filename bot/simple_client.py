from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.types import Message


class SimpleClient(Client):

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(name=bot_name, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    async def send_text_message(self, incoming_message: Message, text: str):
        return await self.send_message(chat_id=incoming_message.chat.id,
                                       reply_to_message_id=incoming_message.id,
                                       text=text)

    async def edit_text_message(self, incoming_message: Message, text: str):
        return await self.edit_message_text(chat_id=incoming_message.chat.id,
                                            message_id=incoming_message.reply_to_message_id,
                                            text=text)


