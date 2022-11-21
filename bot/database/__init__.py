from pymongo.cursor import Cursor

from bot.database._connection import get_schedule_sessions, get_gmail_sessions

CHAT_ID = "chat_id"
SCHEDULE = "schedule"
APP_PASSWORD = 'app_password'
GMAIL_ADDRESS = "gmail_address"
MODULE_IS_ON = 'module_is_on'


def get_schedule_by_chat_id(chat_id: int) -> list:
    """
    :param chat_id:
    :return: schedule - list with pairs
    """
    return get_schedule_sessions().find_one({CHAT_ID: chat_id}).get(SCHEDULE)


def upsert_schedule(chat_id: int, schedule: list, module_is_on: bool = True) -> int:
    a = get_schedule_sessions().update_one({CHAT_ID: chat_id},
                                              {"$set": {
                                                  SCHEDULE: schedule,
                                                  MODULE_IS_ON: module_is_on
                                              }
                                              },
                                              upsert=True)
    return a

def get_gmail_address_and_app_password_by_chat_id(chat_id: int) -> tuple[str, str] | None:
    result = get_gmail_sessions().find_one({CHAT_ID: chat_id})
    if result is None:
        return None
    return result.get(GMAIL_ADDRESS), result.get(APP_PASSWORD)


def update_gmail_module(chat_id: int, module_is_on: bool) -> bool:
    return get_gmail_sessions().update_one({CHAT_ID: chat_id},
                                           {"$set": {MODULE_IS_ON: module_is_on}}).matched_count == 1


def upsert_gmail(chat_id: int, gmail_address: str, app_password: str, module_is_on: bool = True) -> bool:
    return get_gmail_sessions().update_one({CHAT_ID: chat_id},
                                           {"$set": {
                                               GMAIL_ADDRESS: gmail_address,
                                               APP_PASSWORD: app_password,
                                               MODULE_IS_ON: module_is_on
                                           }},
                                           upsert=True).matched_count == 1


def get_all_gmail_sessions() -> Cursor:
    return get_gmail_sessions().find()


def get_all_schedule_sessions() -> Cursor:
    return get_schedule_sessions().find()
