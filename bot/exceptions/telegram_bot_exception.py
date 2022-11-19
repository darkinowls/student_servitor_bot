class TelegramBotException(Exception):

    def __init__(self, text):
        super().__init__(text)
        self.__text = text

    def __str__(self):
        return self.__text
