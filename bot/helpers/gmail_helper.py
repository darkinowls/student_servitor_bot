import re

from schedule import Job

from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.list_helper import get_parameters_list

GMAIL_REGEX = r"^[a-z0-9](\.?[a-z0-9]){5,}@gmail\.com$"
CHECK_BOX_EMOJI = '\U00002705'


def get_email_address_and_app_password_from_parameters(text: str) -> tuple[str, str]:
    index_list: list[str] = get_parameters_list(text)
    if len(index_list) != 2:
        raise TelegramBotException("Have to be 2 parameters: email address and password")
    email_address: str = index_list[0]
    if not re.match(GMAIL_REGEX, email_address):
        raise TelegramBotException(f"The {email_address} email address is a not gmail address")
    password: str = index_list[1]
    if len(password) != 16:
        raise TelegramBotException("The App password must have exactly 16 chars")
    return email_address, password


def check_gmail_job(gmail_job: Job):
    if gmail_job is None:
        raise TelegramBotException("No gmail connection in this chat")
