from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from bot.constants.database import CHAT_ID, GMAIL_ADDRESS, APP_PASSWORD, MODULE_IS_ON, SCHEDULE, SET_COMMAND, ID, \
    GMAIL_SESSIONS, STUDENT_BOT, SCHEDULE_SESSIONS
from bot.constants.load_env import CONNECTION_STRING


def __get_database() -> Database:
    return MongoClient(CONNECTION_STRING).get_database(STUDENT_BOT)


def __get_gmail_sessions_collection() -> Collection:
    return __get_database().get_collection(GMAIL_SESSIONS)


def __get_schedule_sessions_collection() -> Collection:
    return __get_database().get_collection(SCHEDULE_SESSIONS)


def update_gmail_module(chat_id: int, module_is_on: bool) -> bool:
    return __get_gmail_sessions_collection().update_one({CHAT_ID: chat_id},
                                                        {SET_COMMAND: {MODULE_IS_ON: module_is_on}}).matched_count == 1


def update_schedule_module(chat_id: int, module_is_on: bool) -> bool:
    return __get_schedule_sessions_collection().update_one({CHAT_ID: chat_id},
                                                           {SET_COMMAND: {
                                                               MODULE_IS_ON: module_is_on}}).matched_count == 1


def upsert_gmail(chat_id: int, gmail_address: str, app_password: str, module_is_on: bool = True) -> bool:
    return __get_gmail_sessions_collection().update_one({CHAT_ID: chat_id},
                                                        {SET_COMMAND: {
                                                            GMAIL_ADDRESS: gmail_address,
                                                            APP_PASSWORD: app_password,
                                                            MODULE_IS_ON: module_is_on
                                                        }},
                                                        upsert=True).matched_count == 1


def upsert_schedule(chat_id: int, schedule: list[dict], module_is_on: bool = True) -> bool:
    return __get_schedule_sessions_collection().update_one({CHAT_ID: chat_id},
                                                           {SET_COMMAND: {
                                                               SCHEDULE: schedule,
                                                               MODULE_IS_ON: module_is_on
                                                           }},
                                                           upsert=True).matched_count == 1


def get_all_gmail_sessions() -> Cursor:
    return __get_gmail_sessions_collection().find()


def get_all_schedule_sessions() -> Cursor:
    return __get_schedule_sessions_collection().find()


def get_schedule_and_module_is_on_by_chat_id(chat_id: int) -> tuple[str | None, bool | None]:
    result: dict = __get_schedule_sessions_collection().find_one(
        {CHAT_ID: chat_id},
        {SCHEDULE: 1, MODULE_IS_ON: 1, ID: 0}
    )
    return result.get(SCHEDULE), result.get(MODULE_IS_ON)


def get_gmail_address_and_module_is_on_by_chat_id(chat_id: int) -> tuple[str | None, bool | None]:
    result: dict = __get_gmail_sessions_collection().find_one(
        {CHAT_ID: chat_id},
        {GMAIL_ADDRESS: 1, MODULE_IS_ON: 1, ID: 0}
    )
    return result.get(GMAIL_ADDRESS), result.get(MODULE_IS_ON)
