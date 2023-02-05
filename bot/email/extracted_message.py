import re

from bot.constants.emoji import ENVELOPE_EMOJI
from bot.constants.general import EMPTY_STR, RETURN, END_LINE, COLON, WHITESPACE, THREE_DOTS
from bot.constants.gmail import SUBJECT, NAME, EMAIL, PLAIN, RECEIVER, SUBJECT_UPPER, ATTACHMENTS, \
    GMAIL_COM_SEARCH_TEMPLATE, UNICODE_ESCAPE
from bot.constants.regex import UTF_16_REGEX, URL_BAD_SIGNS_REGEX


class ExtractedMessage:
    subject: str | None
    sender_email: str
    sender_name: str
    text: str | None
    receiver_email: str
    attachments: list[dict]

    def __init__(self, message):

        self.subject = None
        if hasattr(message, SUBJECT):
            self.subject = message.subject
            self.subject = self.subject.replace(END_LINE, EMPTY_STR)

        self.text: str = "HTML message is sent. Check link down below."
        if len(message.body[PLAIN]) > 0:
            self.text: str = self.__parse_text(message.body[PLAIN][0])

        self.sender_name: str = message.sent_from[0][NAME]
        self.sender_email: str = message.sent_from[0][EMAIL]
        self.receiver_email = message.sent_to[0][EMAIL]
        self.attachments: list[dict] = message.attachments

    def __str__(self) -> str:
        result_str: str = ENVELOPE_EMOJI + WHITESPACE + self.sender_name + WHITESPACE + self.sender_email + END_LINE
        result_str += RECEIVER + COLON + self.receiver_email + END_LINE
        result_str += SUBJECT_UPPER + COLON + self.subject + END_LINE if self.subject else EMPTY_STR
        result_str += END_LINE + self.text + END_LINE if self.text else EMPTY_STR
        result_str += END_LINE + ATTACHMENTS + COLON + len(self.attachments).__str__() + END_LINE if len(
            self.attachments) != 0 else EMPTY_STR
        result_str += END_LINE + GMAIL_COM_SEARCH_TEMPLATE + self.__create_search_url() + END_LINE

        return result_str

    @staticmethod
    def __parse_text(text: str | bytes) -> str:
        # if text is big
        if len(text) > 1000:
            text = text[:1000]

        if type(text) == bytes:
            text: str = text.decode()
        else:
            text: str = ExtractedMessage.__encode_decode_UTF_16_text(text)

        text = text.replace(END_LINE, WHITESPACE)
        text = text.strip()
        text = text.replace(RETURN, EMPTY_STR)

        # if text is still big
        if len(text) > 150:
            text = text[:150] + THREE_DOTS
        return text

    @staticmethod
    def __encode_decode_UTF_16_text(text: str) -> str:
        # if text has utf-16
        for match in re.finditer(UTF_16_REGEX, text):
            elem = match.group(0)
            text = text.replace(elem, elem.encode().decode(UNICODE_ESCAPE))
        return text

    def __create_search_url(self) -> str:
        if not self.subject:
            return self.sender_email
        return self.__clean_text_for_url(self.subject)

    @staticmethod
    def __clean_text_for_url(text: str) -> str:
        return '+'.join(re.sub(URL_BAD_SIGNS_REGEX, EMPTY_STR, text).split())
