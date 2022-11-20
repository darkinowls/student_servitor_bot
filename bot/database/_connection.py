from pymongo import MongoClient
from pymongo.collection import Collection
from bot import CONNECTION_STRING
from pymongo.database import Database


def get_database() -> Database:
    return MongoClient(CONNECTION_STRING).get_database("student_bot")


def get_gmail_sessions() -> Collection:
    return get_database().get_collection("gmail_sessions")


def get_schedule_sessions() -> Collection:
    return get_database().get_collection("schedule_sessions")
