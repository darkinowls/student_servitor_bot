import re

from bot.constants.regex import GMAIL_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.parameter_helper import get_parameters_list


def get_gmail_address_and_app_password_from_parameters(text: str) -> tuple[str, str]:
    index_list: list[str] = get_parameters_list(text)
    if len(index_list) != 2:
        raise TelegramBotError("Потребуються 2 параметри: gmail адреса та пароль додатку (App password)")
    gmail_address: str = index_list[0]
    if not re.match(GMAIL_REGEX, gmail_address):
        raise TelegramBotError(f"{gmail_address} не є gmail адресою")
    password: str = index_list[1]
    if len(password) != 16:
        raise TelegramBotError("Пароль додатку (App password) має складатися з 16 символів")
    return gmail_address, password
