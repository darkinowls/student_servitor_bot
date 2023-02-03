import json
from pyrogram.types import Document

from bot.constants.database import SCHEDULE
from bot.exceptions.telegram_bot_error import TelegramBotError


def check_document_is_json(document: Document) -> bool:
    if document is None or not document.file_name.endswith(".json"):
        raise TelegramBotError("Json document is required")
    return True


def load_schedule_json_from_file(filepath) -> list[dict]:
    try:
        with open(filepath) as f:
            return json.load(f).get(SCHEDULE)
    except ValueError:
        raise TelegramBotError('JSON syntax error')
    except KeyError:
        raise TelegramBotError('No field "schedule" in the json')


def get_from_json(key: str, json_dict: dict):
    try:
        return json_dict.get(key)
    except KeyError:
        raise TelegramBotError("No key such as " + key)
