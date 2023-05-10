import re

from bot.constants.regex import RECORD_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.parameter_helper import get_parameters_list, check_param_size


def create_record(text: str) -> tuple[int | None, str]:
    check_param_size(text)
    match = re.search('^' + RECORD_REGEX + '$', text)
    if not match:
        raise TelegramBotError("Введіть додатній індекс та назву, аби створити запис у черзі. Принаймні назву")

    record_index: int | None = __parse_record_index(match.group(1))

    record_value: str = match.group(4)
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
            index:int = __parse_record_index(param)
            index_list.append(index)
        return index_list
    except ValueError:
        raise TelegramBotError("Введіть числа")


def parse_index_ranges(parameters: list[str]) -> list[str]:
    two_dots_index: int = parameters.index("..")
    try:
        next_int: int = __parse_record_index(parameters[two_dots_index + 1])
        prev_int: int = __parse_record_index(parameters[two_dots_index - 1])
        if prev_int >= next_int:
            raise TelegramBotError("Перше число має бути менше ніж друге у .. виразі")
    except (ValueError, IndexError):
        raise TelegramBotError("Введіть два числа у .. виразі")

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
        raise TelegramBotError("Введіть два індекса")
    first = index_list[0]
    second = index_list[1]
    if first == second:
        raise TelegramBotError("Одинакові індекси")
    return first, second


def __parse_record_index(record_index_str: str | None) -> int | None:
    if record_index_str is None:
        return None
    record_index = int(record_index_str)
    if record_index and record_index >= 1000:
        raise TelegramBotError("Надто великий індекс. Має бути менше 1000")
    return record_index
