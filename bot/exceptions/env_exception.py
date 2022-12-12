class EnvException(Exception):

    def __init__(self, text):
        self.__text = text
        super().__init__(self.__text)

    def __str__(self):
        return self.__text
