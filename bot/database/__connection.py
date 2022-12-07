from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from bot.constants.database import STUDENT_BOT, GMAIL_SESSIONS, SCHEDULE_SESSIONS
from bot.constants.load_env import CONNECTION_STRING




def __get_database() -> Database:
    return MongoClient(CONNECTION_STRING).get_database(STUDENT_BOT)


def __get_gmail_sessions_collection() -> Collection:
    return __get_database().get_collection(GMAIL_SESSIONS)


def __get_schedule_sessions_collection() -> Collection:
    return __get_database().get_collection(SCHEDULE_SESSIONS)
