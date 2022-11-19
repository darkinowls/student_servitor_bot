import imaplib

from imbox import Imbox
from bot.email.message import Message
from bot.exceptions.telegram_bot_exception import TelegramBotException

IMAP_SERVER = "imap.gmail.com"


def test_connection(email_address: str, password: str):
    try:
        Imbox(IMAP_SERVER, username=email_address, password=password)
    except imaplib.IMAP4.error:
        raise TelegramBotException('The authentication has been failed. Please check the docs')


def get_messages(email_address: str, password: str) -> list[str]:
    texts: list[str] = []
    with Imbox(IMAP_SERVER, username=email_address, password=password) as imbox:
        for uid, message in imbox.messages(unread=True):
            message = Message(message)
            texts.append(message.__str__())
            imbox.mark_seen(uid)
    return texts
