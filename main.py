from bot.constants.load_env import API_ID, API_HASH, BOT_TOKEN
from bot.modules import TelegramBot

if __name__ == "__main__":
    telegram_bot = TelegramBot(api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    telegram_bot.run()
