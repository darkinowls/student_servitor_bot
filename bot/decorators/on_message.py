from typing import Callable
from bot.simple_client import SimpleClient


def on_message(self=SimpleClient, filters=None, group: int = 0) -> Callable:
    def decorator(func):
        @self.on_message(filters, group)
        async def register_function(client, message):
            await client.run_wrapped_function(message, func)

    return decorator

