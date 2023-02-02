from bot.constants.emoji import RED_CROSS_EMOJI, WARNING_EMOJI
from bot.constants.general import WHITESPACE
from bot.exceptions.telegram_bot_exception import TelegramBotException


class TelegramBotWarning(TelegramBotException):

    def __init__(self, text):
        super().__init__(WARNING_EMOJI + WHITESPACE + text)
