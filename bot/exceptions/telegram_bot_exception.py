class TelegramBotException(Exception):
    __RED_CROSS_EMOJI = '\U0000274C'

    def __init__(self, text):
        self.__text = self.__RED_CROSS_EMOJI + " " + text
        super().__init__(self.__text)

    def __str__(self):
        return self.__text
