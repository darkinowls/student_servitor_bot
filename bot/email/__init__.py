import imaplib

from imbox import Imbox
from bot.email.extracted_message import ExtractedMessage
from bot.exceptions.telegram_bot_exception import TelegramBotException


class GmailClient:
    __IMAP_SERVER: str = "imap.gmail.com"
    __imbox: Imbox

    def __init__(self, email_address: str, password: str):
        try:
            self.__imbox = Imbox(self.__IMAP_SERVER, username=email_address, password=password)
        except imaplib.IMAP4.error:
            raise TelegramBotException('The authentication has been failed. Please check the docs')

    def get_new_messages(self) -> list[str]:
        texts: list[str] = []
        for uid, message in self.__imbox.messages(unread=True):
            e_message = ExtractedMessage(message)
            texts.append(e_message.__str__())
            self.__imbox.mark_seen(uid)
        return texts
