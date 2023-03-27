import re

from bot.constants.regex import RECORD_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.parameter_helper import get_parameters_list, check_param_size


def create_record(text: str) -> tuple[int | None, str]:
    check_param_size(text)
    match = re.search('^' + RECORD_REGEX + '$', text)
    if not match:
        raise TelegramBotError("Enter index and name to create a record in the queue. At least name")

    record_index: int = match.group(1)
    __check_record_index(record_index)

    record_value: str = match.group(2)
    return record_index, record_value


def get_index_list_from_parameters(text: str) -> list[int]:
    parameters: list[str] = get_parameters_list(text)
    if '..' in parameters:
        parameters: list[str] = parse_index_ranges(parameters)
    return parse_str_list_to_int_list(parameters)


def parse_str_list_to_int_list(parameters: list[str]) -> list[int]:
    try:
        index_list: list[int] = []
        for param in parameters:
            index = int(param)
            __check_record_index(index)
            index_list.append(index)
        return index_list
    except ValueError:
        raise TelegramBotError("Enter integers")


def parse_index_ranges(parameters: list[str]) -> list[str]:
    two_dots_index: int = parameters.index("..")
    try:
        next_int: int = int(parameters[two_dots_index + 1])
        prev_int: int = int(parameters[two_dots_index - 1])
        __check_record_index(next_int)
        if prev_int >= next_int:
            raise TelegramBotError("The first number should be less than the second in .. expression")
    except (ValueError, IndexError):
        raise TelegramBotError("Enter two integers between .. expression")

    sliced_prev_list, sliced_next_list = parameters[:two_dots_index - 1], parameters[two_dots_index + 1:]
    casted_list: list[str] = [str(i) for i in range(prev_int, next_int)]
    sliced_prev_list.extend(casted_list)
    sliced_prev_list.extend(sliced_next_list)
    if '..' in sliced_prev_list:
        return parse_index_ranges(sliced_prev_list)
    return sliced_prev_list


def get_two_unique_indexes_from_parameters(text: str) -> tuple[int, int]:
    parameters: list[str] = get_parameters_list(text)
    index_list: list[int] = parse_str_list_to_int_list(parameters)
    if len(index_list) != 2:
        raise TelegramBotError("Type 2 indexes")
    first = index_list[0]
    second = index_list[1]
    if first == second:
        raise TelegramBotError("The same indexes")
    return first, second


def __check_record_index(record_index: int):
    if record_index and record_index >= 1000:
        raise TelegramBotError("To big index. It should be less 1000")
