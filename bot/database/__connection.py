from pymongo import MongoClient
from pymongo.collection import Collection
from bot import CONNECTION_STRING
from pymongo.database import Database


def __get_database() -> Database:
    return MongoClient(CONNECTION_STRING).get_database("student_bot")


def __get_gmail_sessions_collection() -> Collection:
    return __get_database().get_collection("gmail_sessions")


def __get_schedule_sessions_collection() -> Collection:
    return __get_database().get_collection("schedule_sessions")
