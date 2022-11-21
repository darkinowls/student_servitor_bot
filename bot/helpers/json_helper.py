import json
from typing import BinaryIO
from pyrogram.types import Document
from bot.exceptions.telegram_bot_exception import TelegramBotException


def check_document_is_json(document: Document) -> bool:
    if document is None or not document.file_name.endswith(".json"):
        raise TelegramBotException("Json document is required")
    return True


# def create_json_from_binary_io(stream: BinaryIO) -> dict:
#     chars: str = stream.read().decode()
#     try:
#         json_dict = json.loads(chars)
#     except Exception:
#         raise TelegramBotException("Json has errors")
#     return json_dict

def load_json_file(filepath) -> dict:
    try:
        with open(filepath) as f:
            return json.load(f)
    except ValueError:
        TelegramBotException('JSON syntax error')