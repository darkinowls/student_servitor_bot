from typing import Callable

from pyrogram.types import CallbackQuery

from bot.modules.simple_client import SimpleClient


def on_callback_query(self=SimpleClient, filters=None, group: int = 0) -> Callable:
    def decorator(func):
        @self.on_callback_query(filters, group)
        async def register_function(client, callback_query: CallbackQuery):
            callback_query.message.text = callback_query.data
            await client.run_wrapped_function(callback_query.message, func)

    return decorator