import re


class ExtractedMessage:
    subject: str
    sender_email: str
    sender_name: str
    text: str
    receiver_email: str
    attachments: list[dict]
    __UTF_16_REGEX = r"\\u\d{3}\w"

    def __init__(self, message):
        self.subject = message.subject if hasattr(message, 'subject') else ""
        self.sender_name: str = message.sent_from[0]['name']
        self.sender_email: str = message.sent_from[0]['email']
        self.receiver_email = message.sent_to[0]['email']
        self.text: str = self.__parse_text(message.body['plain'][0])
        self.attachments: list[dict] = message.attachments

    def __str__(self) -> str:
        result_str: str = ""
        result_str += "Sender: " + self.sender_name + " " + self.sender_email + "\n"
        result_str += "Receiver: " + self.receiver_email + "\n"
        result_str += "Subject: " + self.subject + "\n" if self.subject != "" else ""
        result_str += "Attachments: " + len(self.attachments).__str__() + "\n" if len(
            self.attachments) != 0 else ""
        result_str += "Text: " + self.text + "\n" if self.text != "" else ""
        result_str += "Reference: https://mail.google.com/mail/u/0/\n"

        return result_str


    def __parse_text(self, text: str) -> str:
        text = text.replace('\r', '')
        text = text.replace('\n', ' ')
        text = text.strip()

        # if text has utf-16
        for match in re.finditer(self.__UTF_16_REGEX, text):
            elem = match.group(0)
            text = text.replace(elem, elem.encode().decode("unicode_escape"))

        # if text is big
        if len(text) > 200:
            text = text[:200] + "..."
        return text
