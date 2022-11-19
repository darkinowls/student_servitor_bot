from bot.database._connection import get_schedule_sessions, get_gmail_sessions


def get_schedule_by_chat_id(self, chat_id: int) -> dict:
    return get_schedule_sessions().find_one({"chat_id": chat_id}).get("schedule")


def upsert_schedule(chat_id: int, schedule: dict) -> int:
    return get_schedule_sessions().update_one({"chat_id": chat_id},
                                              {"$set": {"schedule": schedule}},
                                              upsert=True).matched_count


def get_gmail_api_by_chat_id(chat_id: int) -> dict:
    return get_gmail_sessions().find_one({"chat_id": chat_id}).get("installed")


def upsert_gmail(chat_id: int, installed: dict):
    return get_schedule_sessions().update_one({"chat_id": chat_id},
                                              {"$set": {"installed": installed}},
                                              upsert=True).matched_count
