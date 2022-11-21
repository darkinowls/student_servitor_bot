import os


def get_or_create_tmp_json_file(filename: str, chat_id: int, text: str = None) -> str:
    filepath = generate_tmp_filepath(filename, chat_id)
    if not os.path.isfile(filepath):
        _create_file(filepath, text)
    return filepath


def generate_tmp_filepath(filename, chat_id) -> str:
    os.makedirs(".tmp", exist_ok=True)
    return ".tmp/" + filename + "_" + chat_id.__str__() + ".json"


def _create_file(filepath, text) -> int:
    with open(filepath, mode="w", encoding="utf-8") as json_file:
        return json_file.write(text.__str__())
