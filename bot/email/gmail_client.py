import imaplib

from imbox import Imbox

from bot.constants.gmail import IMAP_GMAIL_SERVER
from bot.email.extracted_message import ExtractedMessage
from bot.exceptions.telegram_bot_exception import TelegramBotException


class GmailClient:

    __imbox: Imbox

    def __init__(self, email_address: str, password: str):
        try:
            self.__imbox = Imbox(IMAP_GMAIL_SERVER, username=email_address, password=password)
        except imaplib.IMAP4.error:
            raise TelegramBotException('The authentication has been failed.\n'
                                       'Please check the gmail module docs:\n'
                                       'https://github.com/Darkinowls/student_servitor_bot')

    def get_new_messages(self) -> list[str]:
        texts: list[str] = []
        for uid, message in self.__imbox.messages(unread=True):
            e_message = ExtractedMessage(message)
            texts.append(e_message.__str__())
            self.__imbox.mark_seen(uid)
        return texts
