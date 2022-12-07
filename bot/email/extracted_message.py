import re

from bot.constants.general import EMPTY_STR, RETURN, END_LINE, COLON, WHITESPACE, THREE_DOTS
from bot.constants.gmail import SUBJECT, NAME, EMAIL, PLAIN, SENDER, RECEIVER, SUBJECT_UPPER, ATTACHMENTS, TEXT, \
    GMAIL_COM_REFERENCE, UNICODE_ESCAPE
from bot.constants.regex import UTF_16_REGEX




class ExtractedMessage:
    subject: str
    sender_email: str
    sender_name: str
    text: str
    receiver_email: str
    attachments: list[dict]

    def __init__(self, message):
        self.subject = message.subject if hasattr(message, SUBJECT) else EMPTY_STR
        self.sender_name: str = message.sent_from[0][NAME]
        self.sender_email: str = message.sent_from[0][EMAIL]
        self.receiver_email = message.sent_to[0][EMAIL]
        self.text: str = self.__parse_text(message.body[PLAIN][0])
        self.attachments: list[dict] = message.attachments

    def __str__(self) -> str:
        result_str: str = EMPTY_STR
        result_str += SENDER + COLON + self.sender_name + WHITESPACE + self.sender_email + END_LINE
        result_str += RECEIVER + COLON + self.receiver_email + END_LINE
        result_str += SUBJECT_UPPER + COLON + self.subject + END_LINE if self.subject != EMPTY_STR else EMPTY_STR
        result_str += ATTACHMENTS + COLON + len(self.attachments).__str__() + END_LINE if len(
            self.attachments) != 0 else EMPTY_STR
        result_str += TEXT + COLON + self.text + END_LINE if self.text != EMPTY_STR else EMPTY_STR
        result_str += GMAIL_COM_REFERENCE + END_LINE

        return result_str

    @staticmethod
    def __parse_text(text: str) -> str:
        text = text.replace(RETURN, EMPTY_STR)
        text = text.replace(END_LINE, WHITESPACE)
        text = text.strip()

        # if text has utf-16
        for match in re.finditer(UTF_16_REGEX, text):
            elem = match.group(0)
            text = text.replace(elem, elem.encode().decode(UNICODE_ESCAPE))

        # if text is big
        if len(text) > 200:
            text = text[:200] + THREE_DOTS
        return text