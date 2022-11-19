from bot.modules.gmail_module import GmailBot
from bot.modules.list_module import ListBot
from bot.modules.schedule_module import ScheduleBot
from bot import API_ID, BOT_NAME, API_HASH, BOT_TOKEN


class TelegramBot(
    GmailBot,
    ListBot,
    ScheduleBot
):
    pass
    # def __init__(bot_name, api_id, api_hash, bot_token ):
    #     try:
    #         super().__init__(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    #     except TelegramBotException as e:
    #


telegram_bot = TelegramBot(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
