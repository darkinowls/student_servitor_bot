from bot.database._connection import get_schedule_sessions, get_gmail_sessions


def get_schedule_by_chat_id(chat_id: int) -> list:
    """
    :param chat_id:
    :return: schedule - list with pairs
    """
    return get_schedule_sessions().find_one({"chat_id": chat_id}).get("schedule")


def upsert_schedule(chat_id: int, schedule: list) -> int:
    return get_schedule_sessions().update_one({"chat_id": chat_id},
                                              {"$set": {"schedule": schedule}},
                                              upsert=True).matched_count


def get_gmail_address_and_app_password_by_chat_id(chat_id: int) -> tuple[str, str] | None:
    result = get_gmail_sessions().find_one({"chat_id": chat_id})
    if result is None:
        return None
    return result.get("email_address"), result.get("app_password")


def upsert_gmail(chat_id: int, email_address: str, app_password: str) -> bool:
    return get_gmail_sessions().update_one({"chat_id": chat_id},
                                              {"$set": {
                                                  "email_address": email_address,
                                                  "app_password": app_password,
                                              }},
                                              upsert=True).matched_count == 1
