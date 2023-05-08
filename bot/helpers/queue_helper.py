import re
from collections import OrderedDict

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.emoji import SCROLL_EMOJI
from bot.constants.general import END_LINE
from bot.constants.help_alerts import SWAP_HELP, RM_HELP, HEADER_HELP, ADD_HELP, HOW_TO_SWAP, HOW_TO_REMOVE, \
    HOW_TO_SET_HEADER, HOW_TO_ADD
from bot.constants.regex import RECORD_REGEX, END_LINE_BEHIND_REGEX, END_AHEAD_REGEX
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.modules.simple_client import SimpleClient


def add_record_to_record_dict(record_dict: OrderedDict, record_index: int | None, record_value: str) -> OrderedDict:
    if len(record_dict) > 256:
        raise TelegramBotError("Черга повна. 256 записів - це максимум")

    # if queue is empty then insert as the first one
    if len(record_dict) == 0 and record_index is None:
        return OrderedDict({0: record_value})

    # if no index then add as the last one
    if record_index is None:
        record_index: int = list(record_dict.keys())[-1] + 1
        record_dict[record_index] = record_value
        return record_dict

    # if index is occupied then error else set
    if record_index in record_dict.keys():
        raise TelegramBotError("Індекс занятий")
    else:
        record_dict[record_index] = record_value
        return record_dict


async def check_reply_to_my_queue_message(_, client: SimpleClient, message: Message, raiseable: bool = False) -> bool:
    """
    Function for a filter, or it checks, when raiseable=True
    :param _:
    :param client:
    :param message:
    :param raiseable:
    :return:
    """
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


def get_order_record_dict_and_header_from_queue(reply_to_message_text: str) -> tuple[OrderedDict[int, str], str]:
    record_dict = OrderedDict()
    for record in re.finditer(END_LINE_BEHIND_REGEX + RECORD_REGEX + END_AHEAD_REGEX, reply_to_message_text):
        record_index, record_value = record.groups()
        record_dict[int(record_index)] = record_value
    return record_dict, reply_to_message_text.split(END_LINE, 1)[0]


def format_to_text(record_dict: OrderedDict[int, str], header: str) -> str:
    """
    Function formats a record dict and header to a single text
    :param record_dict:
    :param header:
    :return:
    """
    student_queue_text: str = header + END_LINE
    for record_index, record_value in sorted(record_dict.items()):
        student_queue_text += str(record_index) + '. ' + record_value + END_LINE
    return student_queue_text


def remove_records_by_indexes(index_list: list[int], record_dict: OrderedDict) -> OrderedDict:
    no_changes: bool = [record_dict.pop(index) for index in index_list if index in record_dict.keys()] == []
    if no_changes is True:
        raise TelegramBotError("No such indexes")
    return record_dict


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
