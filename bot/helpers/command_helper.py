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
    parameters_list: list[str] = []
    for parameter in text.split(' ')[1:]:
        if parameter == '':
            continue
        __check_param_size(parameter)
        parameters_list.append(parameter)
    return parameters_list


def get_single_text_parameter(text: str, should_exist: bool = True) -> str:
    """
     /swap 1 2 - query
     /swap - command
     1 2 - single text parameter
     :param should_exist: bool = True. If the param should exist
     :param text: str
     :return: params
     """
    try:
        parameter: str = text.strip().split(' ', 1)[1].strip()
        __check_param_size(parameter)
        return parameter
    except IndexError:
        if not should_exist:
            return ''
        raise TelegramBotException("No parameter")


def __check_param_size(parameter: str):
    if len(parameter) > 100:
        raise TelegramBotException("Too big parameter")
