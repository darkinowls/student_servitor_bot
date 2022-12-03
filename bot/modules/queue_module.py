from collections import OrderedDict

from pyrogram import filters
from pyrogram.filters import Filter

from bot.decorators.on_typed_message import on_typed_message
from bot.modules.basic_bot import BasicBot
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.command_helper import get_single_text_parameter
from bot.helpers.queue_helper import Message, \
    get_order_records_dict_and_header, \
    create_queue_text, SCROLL_EMOJI, is_reply_to_my_queue_message, get_index_list_from_parameters, \
    get_two_indexes_from_parameters, \
    swap_records_by_indexes, remove_records_by_indexes, create_record


class QueueModule(BasicBot):

    async def edit_student_queue(self, record_dict: OrderedDict, header: str, original_message: Message):
        queue_text: str = create_queue_text(record_dict, header)
        await self.edit_text_message(original_message,
                                     text=queue_text)

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        reply_to_my_list_message_filter: Filter = filters.create(is_reply_to_my_queue_message)

        @on_typed_message(self, filters.command("rm") & reply_to_my_list_message_filter)
        async def remove_by_indexes(_, message: Message):
            index_list: list[int] = get_index_list_from_parameters(message.text)
            record_dict, header = get_order_records_dict_and_header(message.text)
            record_dict: OrderedDict = remove_records_by_indexes(index_list, record_dict)
            await self.edit_student_queue(record_dict, header, original_message=message)

        @on_typed_message(self, filters.command("swap") & reply_to_my_list_message_filter)
        async def swap_by_index(_, message: Message):
            first, second = get_two_indexes_from_parameters(message.text)
            record_dict, header = get_order_records_dict_and_header(message.text)
            record_dict: OrderedDict = swap_records_by_indexes(first, second, record_dict)
            await self.edit_student_queue(record_dict, header, original_message=message)

        @on_typed_message(self, filters.command("header") & reply_to_my_list_message_filter)
        async def set_header(_, message: Message):
            new_header: str = SCROLL_EMOJI + ' ' + get_single_text_parameter(message.text)
            record_dict, _ = get_order_records_dict_and_header(message.text)
            await self.edit_student_queue(record_dict, header=new_header, original_message=message)

        @on_typed_message(self, filters.command("queue"))
        async def create_queue(_, message: Message):
            header: str = get_single_text_parameter(message.text, should_exist=False)
            header = SCROLL_EMOJI + ' ' + header
            await self.send_reply_message(message, text=header)

        @on_typed_message(self, reply_to_my_list_message_filter)
        async def add_to_queue(_, message: Message):
            record_index, record_value = create_record(message.text)
            record_dict, header = get_order_records_dict_and_header(message.text)

            # if queue is empty
            if len(record_dict) == 0:
                return self.edit_student_queue(OrderedDict({1: record_value}), header, original_message=message)

            # if no index
            if record_index is None:
                record_index: int = list(record_dict.keys())[-1] + 1
                record_dict[record_index] = record_value
                return self.edit_student_queue(record_dict, header, original_message=message)

            # if index is occupied
            if record_index in record_dict.keys():
                raise TelegramBotException("Index is occupied")
            record_dict[record_index] = record_value

            return self.edit_student_queue(record_dict, header, original_message=message)
