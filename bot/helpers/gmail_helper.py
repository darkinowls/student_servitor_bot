import re

from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.list_helper import get_parameters_list

GMAIL_REGEX = r"^[a-z0-9](\.?[a-z0-9]){5,}@gmail\.com$"


def get_email_address_and_password_from_parameters(text: str) -> tuple[str, str]:
    index_list: list[str] = get_parameters_list(text)
    if len(index_list) != 2:
        raise TelegramBotException("Have to be 2 parameters: email address and password")
    email_address: str = index_list[0]
    if not re.match(GMAIL_REGEX, email_address):
        raise TelegramBotException(f"The {email_address} email address is a not gmail address")
    password: str = index_list[1]
    if len(password) != 16:
        raise TelegramBotException(f"The App password must have exactly 16 chars")
    return email_address, password



