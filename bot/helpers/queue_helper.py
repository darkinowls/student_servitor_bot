import re
from collections import OrderedDict
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.emoji import SCROLL_EMOJI
from bot.constants.general import END_LINE
from bot.constants.help_alerts import SWAP_HELP, RM_HELP, HEADER_HELP, ADD_HELP
from bot.constants.regex import RECORD_REGEX, END_LINE_BEHIND_REGEX, END_AHEAD_REGEX
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.command_helper import get_parameters_list
from bot.modules.simple_client import SimpleClient


def create_record(text: str) -> tuple[int | None, str]:
    match = re.search('^' + RECORD_REGEX + '$', text)
    if not match:
        raise TelegramBotException("Enter index and name. At least name")
    record_index: int = int(match.group(1)) if match.group(1) else None
    record_value: str = match.group(2)
    return record_index, record_value


async def is_reply_to_my_queue_message(_, client: SimpleClient, message: Message) -> bool:
    return message.reply_to_message is not None and \
           message.reply_to_message.from_user.username == (await client.get_me()).username and \
           SCROLL_EMOJI in message.reply_to_message.text


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
    try:
        index_list: list[int] = [int(index) for index in parameters]
    except ValueError:
        raise TelegramBotException("Enter integers")
    if not index_list:
        raise TelegramBotException("Enter indexes")
    return index_list


def remove_records_by_indexes(index_list: list[int], record_dict: OrderedDict) -> OrderedDict:
    no_changes: bool = [record_dict.pop(index) for index in index_list if index in record_dict.keys()] == []
    if no_changes is True:
        raise TelegramBotException("No such indexes")
    return record_dict


def get_two_indexes_from_parameters(text: str) -> tuple[int, int]:
    index_list: list[int] = get_index_list_from_parameters(text=text)
    if len(index_list) != 2:
        raise TelegramBotException("Type 2 indexes")
    first = index_list[0]
    second = index_list[1]
    if first == second:
        raise TelegramBotException("The same indexes")
    return first, second


def swap_records_by_indexes(first: int, second: int, record_dict: OrderedDict) -> OrderedDict:
    is_first: bool = first in record_dict.keys()
    is_second: bool = second in record_dict.keys()

    # No index in queue
    if not is_first and not is_second:
        raise TelegramBotException("At least one index have to be in the queue")

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
    swap_help = InlineKeyboardButton("swap", callback_data=SWAP_HELP)
    rm_help = InlineKeyboardButton("remove", callback_data=RM_HELP)
    header_help = InlineKeyboardButton("header", callback_data=HEADER_HELP)
    add_help = InlineKeyboardButton("add", callback_data=ADD_HELP)
    return InlineKeyboardMarkup([
        [swap_help, rm_help],
        [header_help, add_help]
    ])
