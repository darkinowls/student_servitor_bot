from bot.constants.general import WHITESPACE, EMPTY_STR
from bot.exceptions.telegram_bot_error import TelegramBotError


def get_parameters_list(text: str) -> list[str]:
    """
    /swap 1 2 - query
    /swap - command
    1 2 - params
    [1, 2] - list of params
    :param text: str
    :return: list of params
    """
    text = get_single_text_parameter(text)
    parameters_list: list[str] = []
    for parameter in text.split(WHITESPACE):
        if parameter == EMPTY_STR:
            continue
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
        parameter: str = text.strip().split(WHITESPACE, 1)[1].strip()
        check_param_size(parameter)
        return parameter
    except IndexError:
        if not should_exist:
            return EMPTY_STR
        raise TelegramBotError("No parameters!")


def check_param_size(parameter: str):
    if len(parameter) > 100:
        raise TelegramBotError("Too big parameter")
