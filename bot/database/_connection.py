from pymongo import MongoClient
from pymongo.collection import Collection
from bot import CONNECTION_STRING


def get_database():
    return MongoClient(CONNECTION_STRING)


def get_gmail_sessions() -> Collection:
    return get_database().get_collection("gmail_sessions")


def get_schedule_sessions() -> Collection:
    return get_database().get_collection("schedule_sessions")
