import re

from bot.constants.regex import GMAIL_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.parameter_helper import get_parameters_list


def get_gmail_address_and_app_password_from_parameters(text: str) -> tuple[str, str]:
    index_list: list[str] = get_parameters_list(text)
    if len(index_list) != 2:
        raise TelegramBotError("Have to be 2 parameters: email address and App password")
    gmail_address: str = index_list[0]
    if not re.match(GMAIL_REGEX, gmail_address):
        raise TelegramBotError(f"The {gmail_address} email address is a not gmail address")
    password: str = index_list[1]
    if len(password) != 16:
        raise TelegramBotError("The App password must have exactly 16 chars")
    return gmail_address, password
