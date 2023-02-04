import imaplib

from imbox import Imbox

from bot.constants.gmail import IMAP_GMAIL_SERVER
from bot.email.extracted_message import ExtractedMessage
from bot.exceptions.telegram_bot_error import TelegramBotError


class GmailClient:
    __imbox: Imbox

    def __init__(self, email_address: str, password: str):
        try:
            self.__imbox = Imbox(IMAP_GMAIL_SERVER, username=email_address, password=password)
        except imaplib.IMAP4.error:
            raise TelegramBotError('The authentication has been failed.\n'
                                   'Please check the gmail module documentation')

    def get_new_messages(self) -> list[str]:
        texts: list[str] = []
        raw_messages: list = self.__imbox.messages(unread=True)
        if len(raw_messages) == 0:
            return []
        for uid, message in raw_messages[:2]:
            e_message = ExtractedMessage(message)
            texts.append(e_message.__str__())
            self.__imbox.mark_seen(uid)
        return texts
