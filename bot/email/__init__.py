import imaplib

from imbox import Imbox
from bot.email.extracted_message import ExtractedMessage
from bot.exceptions.telegram_bot_exception import TelegramBotException

IMAP_SERVER = "imap.gmail.com"


def get_connection(email_address: str, password: str) -> Imbox:
    try:
        return Imbox(IMAP_SERVER, username=email_address, password=password)
    except imaplib.IMAP4.error:
        raise TelegramBotException('The authentication has been failed. Please check the docs')


def get_new_messages(email_address: str, password: str) -> list[str]:
    texts: list[str] = []
    with Imbox(IMAP_SERVER, username=email_address, password=password) as imbox:
        for uid, message in imbox.messages(unread=True):
            extracted_message = ExtractedMessage(message)
            texts.append(extracted_message.__str__())
            imbox.mark_seen(uid)
    return texts
