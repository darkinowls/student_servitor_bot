from bot.constants.load_env import BOT_NAME, API_ID, API_HASH, BOT_TOKEN
from bot.modules import TelegramBot

if __name__ == "__main__":
    telegram_bot = TelegramBot(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    telegram_bot.run()
