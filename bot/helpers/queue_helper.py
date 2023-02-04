import re
from collections import OrderedDict

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.emoji import SCROLL_EMOJI
from bot.constants.general import END_LINE
from bot.constants.help_alerts import SWAP_HELP, RM_HELP, HEADER_HELP, ADD_HELP, HOW_TO_SWAP, HOW_TO_REMOVE, \
    HOW_TO_SET_HEADER, HOW_TO_ADD
from bot.constants.regex import RECORD_REGEX, END_LINE_BEHIND_REGEX, END_AHEAD_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.command_helper import get_parameters_list, check_param_size
from bot.modules.simple_client import SimpleClient


def create_record(text: str) -> tuple[int | None, str]:
    check_param_size(text)
    match = re.search('^' + RECORD_REGEX + '$', text)
    if not match:
        raise TelegramBotError("Enter index and name to create a record in the queue. At least name")

    record_index = match.group(1)
    if record_index and record_index >= 1000:
        raise TelegramBotError("To big index. It should be less 1000")

    record_value: str = match.group(2)
    return record_index, record_value


async def check_reply_to_my_queue_message(_, client: SimpleClient, message: Message, raiseable: bool = False) -> bool:
    error_str: str | None = None
    if message.reply_to_message is None:
        error_str = "Reply a queue"
    elif message.reply_to_message.from_user.username != (await client.get_me()).username:
        error_str = "Reply a BOT queue"
    elif SCROLL_EMOJI not in message.reply_to_message.text:
        error_str = "The bot message is not a queue"

    if error_str is not None:
        if raiseable:
            raise TelegramBotError(error_str)
        if not raiseable:
            return False

    return True


def get_order_record_dict_and_header(reply_to_message_text: str) -> tuple[OrderedDict[int, str], str]:
    record_dict = OrderedDict()
    for record in re.finditer(END_LINE_BEHIND_REGEX + RECORD_REGEX + END_AHEAD_REGEX, reply_to_message_text):
        record_index, record_value = record.groups()
        record_dict[int(record_index)] = record_value
    return record_dict, reply_to_message_text.split(END_LINE, 1)[0]


def create_queue_text(record_dict: OrderedDict[int, str], header: str) -> str:
    student_queue_text: str = header + END_LINE
    for record_index, record_value in sorted(record_dict.items()):
        student_queue_text += str(record_index) + '. ' + record_value + END_LINE
    return student_queue_text


def get_index_list_from_parameters(text: str) -> list[int]:
    parameters: list[str] = get_parameters_list(text)
    if '..' in parameters:
        parameters: list[str] = parse_index_ranges(parameters)
    try:
        index_list: list[int] = [int(index) for index in parameters]
    except ValueError:
        raise TelegramBotError("Enter integers")
    if not index_list:
        raise TelegramBotError("Enter indexes")
    return index_list


def parse_index_ranges(parameters: list[str]) -> list[str]:
    two_dots_index: int = parameters.index("..")

    try:
        next_int: int = int(parameters[two_dots_index + 1])
        prev_int: int = int(parameters[two_dots_index - 1])
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


def remove_records_by_indexes(index_list: list[int], record_dict: OrderedDict) -> OrderedDict:
    no_changes: bool = [record_dict.pop(index) for index in index_list if index in record_dict.keys()] == []
    if no_changes is True:
        raise TelegramBotError("No such indexes")
    return record_dict


def get_two_indexes_from_parameters(text: str) -> tuple[int, int]:
    index_list: list[int] = get_index_list_from_parameters(text=text)
    if len(index_list) != 2:
        raise TelegramBotError("Type 2 indexes")
    first = index_list[0]
    second = index_list[1]
    if first == second:
        raise TelegramBotError("The same indexes")
    return first, second


def swap_records_by_indexes(first: int, second: int, record_dict: OrderedDict) -> OrderedDict:
    is_first: bool = first in record_dict.keys()
    is_second: bool = second in record_dict.keys()

    # No index in queue
    if not is_first and not is_second:
        raise TelegramBotError("At least one index have to be in the queue")

    # make swap
    if is_first and is_second:
        record_dict[first], record_dict[second] = record_dict[second], record_dict[first]
        return record_dict

    # move record to a new index
    if is_first:
        record_dict[second] = record_dict.pop(first)
    else:
        record_dict[first] = record_dict.pop(second)
    return record_dict


def create_queue_help_markup() -> InlineKeyboardMarkup:
    swap_help = InlineKeyboardButton(HOW_TO_SWAP, callback_data=SWAP_HELP)
    rm_help = InlineKeyboardButton(HOW_TO_REMOVE, callback_data=RM_HELP)
    header_help = InlineKeyboardButton(HOW_TO_SET_HEADER, callback_data=HEADER_HELP)
    add_help = InlineKeyboardButton(HOW_TO_ADD, callback_data=ADD_HELP)
    return InlineKeyboardMarkup([
        [add_help, header_help],
        [rm_help, swap_help]
    ])
