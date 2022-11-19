from bot.exceptions.telegram_bot_exception import TelegramBotException


def get_parameters_list(text: str) -> list[str]:
    """
    /swap 1 2 - query
    /swap - command
    1 2 - params
    [1, 2] - list of params
    :param text: str
    :return: list of params
    """
    return [item for item in text.split(' ')[1:] if item != '']


def get_command(text: str) -> str:
    """
     /swap 1 2 - query
     /swap - command
     1 2 - params
     :param text: str
     :return: command
    """
    return text.strip().split(' ', 1)[0]


def get_parameter(text: str, should_exist: bool = True) -> str:
    """
     /swap 1 2 - query
     /swap - command
     1 2 - params
     :param text: str
     :return: params
     """
    try:
        parameter: str = text.strip().split(' ', 1)[1].strip()
        if len(parameter) > 100:
            raise TelegramBotException("Too big parameter")
        return parameter
    except IndexError:
        if not should_exist:
            return ''
        raise TelegramBotException("No parameter")
