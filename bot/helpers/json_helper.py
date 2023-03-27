import json
import os
import time

from pyrogram.types import Document

from bot.constants.database import SCHEDULE
from bot.constants.general import TMP_FOLDER
from bot.exceptions.telegram_bot_error import TelegramBotError

ENCODING = "utf-8"


def create_tmp_json_file(filename: str, chat_id: int, json_str: str) -> str:
    filepath = create_tmp_json_filepath(filename, chat_id)
    if os.path.isfile(filepath):
        os.remove(filepath)
    __create_json_file(filepath, json_str)
    return filepath


def create_tmp_json_filepath(filename, chat_id) -> str:
    os.makedirs(TMP_FOLDER, exist_ok=True)
    return TMP_FOLDER + filename + "_" + chat_id.__str__() + ".json"


def __create_json_file(filepath: str, json_str: str) -> None:
    json_dict: dict = json.loads(json_str)
    with open(filepath, mode="w", encoding=ENCODING) as json_file:
        json.dump(json_dict, json_file, ensure_ascii=False)


def delete_old_tmp_files(*args: int):
    """
    Deletes files in .tmp folder that is older than *args minutes.
    The function is used by file_garbage_collector.
    :param args: number of minutes
    """
    minutes: int = args[0]
    now_seconds = time.time()
    for filepath in os.listdir(TMP_FOLDER):
        file_seconds = os.path.getmtime(filepath)
        if (now_seconds - file_seconds) / (60 * minutes) > 1:
            os.remove(filepath)


def check_document_is_json(document: Document) -> bool:
    if document is None or not document.file_name.endswith(".json"):
        raise TelegramBotError("Json document is required")
    return True


def load_schedule_json_from_file(filepath: str) -> list[dict]:
    try:
        with open(filepath, mode="r", encoding=ENCODING) as file:
            schedule_list: list[dict] = json.load(file).get(SCHEDULE)
            if len(schedule_list) == 0:
                raise TelegramBotError('Schedule array is empty. Check examples in the documentation')
            return schedule_list
    except ValueError:
        raise TelegramBotError('JSON syntax error')
    except KeyError:
        raise TelegramBotError('No field "schedule" in the json')


def get_from_json(key: str, json_dict: dict):
    try:
        return json_dict.get(key)
    except KeyError:
        raise TelegramBotError("No key such as " + key)
