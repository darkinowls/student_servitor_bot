from pymongo.cursor import Cursor

from bot.database.__connection import __get_schedule_sessions_collection, __get_gmail_sessions_collection

CHAT_ID = "chat_id"
SCHEDULE = "schedule"
APP_PASSWORD = "app_password"
GMAIL_ADDRESS = "gmail_address"
MODULE_IS_ON = "module_is_on"


def update_gmail_module(chat_id: int, module_is_on: bool) -> bool:
    return __get_gmail_sessions_collection().update_one({CHAT_ID: chat_id},
                                                        {"$set": {MODULE_IS_ON: module_is_on}}).matched_count == 1


def update_schedule_module(chat_id: int, module_is_on: bool) -> bool:
    return __get_schedule_sessions_collection().update_one({CHAT_ID: chat_id},
                                                           {"$set": {MODULE_IS_ON: module_is_on}}).matched_count == 1


def upsert_gmail(chat_id: int, gmail_address: str, app_password: str, module_is_on: bool = True) -> bool:
    return __get_gmail_sessions_collection().update_one({CHAT_ID: chat_id},
                                                        {"$set": {
                                                            GMAIL_ADDRESS: gmail_address,
                                                            APP_PASSWORD: app_password,
                                                            MODULE_IS_ON: module_is_on
                                                        }},
                                                        upsert=True).matched_count == 1


def upsert_schedule(chat_id: int, schedule: list[dict], module_is_on: bool = True) -> bool:
    return __get_schedule_sessions_collection().update_one({CHAT_ID: chat_id},
                                                           {"$set": {
                                                               SCHEDULE: schedule,
                                                               MODULE_IS_ON: module_is_on
                                                           }},
                                                           upsert=True).matched_count == 1


def get_all_gmail_sessions() -> Cursor:
    return __get_gmail_sessions_collection().find()


def get_all_schedule_sessions() -> Cursor:
    return __get_schedule_sessions_collection().find()


def get_schedule_by_chat_id(chat_id: int) -> dict | None:
    return __get_schedule_sessions_collection().find_one({"chat_id": chat_id}, {"schedule": 1, "_id": 0})

def get_gmail_address_by_chat_id(chat_id: int) -> str | None:
    return __get_gmail_sessions_collection().find_one({"chat_id": chat_id}, {"gmail_address": 1, "_id": 0})

