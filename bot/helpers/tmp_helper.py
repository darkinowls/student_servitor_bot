import os
import time

from bot import TMP_FOLDER


def get_or_create_tmp_json_file(filename: str, chat_id: int, text: str = None) -> str:
    filepath = generate_tmp_filepath(filename, chat_id)
    if not os.path.isfile(filepath):
        __create_file(filepath, text)
    return filepath


def generate_tmp_filepath(filename, chat_id) -> str:
    os.makedirs(TMP_FOLDER, exist_ok=True)
    return TMP_FOLDER + filename + "_" + chat_id.__str__() + ".json"


def __create_file(filepath, text) -> int:
    with open(filepath, mode="w", encoding="utf-8") as json_file:
        return json_file.write(text.__str__())


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
