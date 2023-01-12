import os
from dotenv import load_dotenv

from bot.exceptions.env_exception import EnvException

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

CONNECTION_STRING = os.getenv("CONNECTION_STRING")

if None in [API_ID, API_HASH, BOT_TOKEN, CONNECTION_STRING]:
    raise EnvException("Set .env file with constants")
