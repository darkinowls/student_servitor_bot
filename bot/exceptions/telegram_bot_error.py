from bot.constants.emoji import RED_CROSS_EMOJI
from bot.constants.general import WHITESPACE
from bot.exceptions.telegram_bot_exception import TelegramBotException


class TelegramBotError(TelegramBotException):

    def __init__(self, text):
        super().__init__(RED_CROSS_EMOJI + WHITESPACE + text)
