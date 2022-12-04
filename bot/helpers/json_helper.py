import json
from pyrogram.types import Document
from bot.exceptions.telegram_bot_exception import TelegramBotException


def check_document_is_json(document: Document) -> bool:
    if document is None or not document.file_name.endswith(".json"):
        raise TelegramBotException("Json document is required")
    return True


def load_schedule_json_from_file(filepath) -> list[dict]:
    try:
        with open(filepath) as f:
            return json.load(f).get('schedule')
    except ValueError:
        raise TelegramBotException('JSON syntax error')
    except KeyError:
        raise TelegramBotException('No field "schedule" in the json')
