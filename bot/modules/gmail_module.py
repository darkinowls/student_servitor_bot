from pyrogram import filters
from pyrogram.types import Message

from bot.modules.basic_module import BasicBot


class GmailBot(BasicBot):

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)

        @self.on_message(filters.command("gmail"))
        @self.on_edited_message(filters.command("gmail"))
        async def set_gmail_api_connection(_, message: Message):
            async def method_name(m: Message):
                pass
                # test_connection()

            await self.wrap_try_except(method_name, message)
