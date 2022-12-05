from bot import API_ID, BOT_NAME, API_HASH, BOT_TOKEN
from bot.modules.basic_module import BasicModule
from bot.modules.queue_module import QueueModule
from bot.modules.scheduled_modules.gmail_module import GmailModule
from bot.modules.scheduled_modules.schedule_module import ScheduleModule


class TelegramBot(
    ScheduleModule,
    GmailModule,
    QueueModule,
    BasicModule
):
    pass


telegram_bot = TelegramBot(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
