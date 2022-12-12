from collections import OrderedDict

from pyrogram import filters
from pyrogram.filters import Filter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.constants.help_alerts import SWAP_HELP, RM_HELP, HEADER_HELP, ADD_HELP, HELP_TITLE
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.command_helper import get_single_text_parameter
from bot.helpers.queue_helper import Message, \
    get_order_record_dict_and_header, \
    create_queue_text, SCROLL_EMOJI, is_reply_to_my_queue_message, get_index_list_from_parameters, \
    get_two_indexes_from_parameters, \
    swap_records_by_indexes, remove_records_by_indexes, create_record, create_queue_help_markup
from bot.modules.simple_client import SimpleClient


class QueueModule(SimpleClient):

    async def __edit_student_queue(self, record_dict: OrderedDict, header: str, incoming_message: Message):
        queue_text: str = create_queue_text(record_dict, header)
        await self.edit_replied_message(incoming_message, queue_text, reply_markup=self.__help_markup)

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        super().__init__(bot_name, api_id, api_hash, bot_token)
        reply_to_my_list_message_filter: Filter = filters.create(is_reply_to_my_queue_message)
        self.__help_markup = create_queue_help_markup()

        @on_typed_message(self, filters.command("rm") & reply_to_my_list_message_filter)
        async def remove_by_indexes(_, message: Message):
            index_list: list[int] = get_index_list_from_parameters(message.text)
            record_dict, header = get_order_record_dict_and_header(message.reply_to_message.text)
            record_dict: OrderedDict = remove_records_by_indexes(index_list, record_dict)
            await self.__edit_student_queue(record_dict, header, incoming_message=message.reply_to_message)

        @on_typed_message(self, filters.command("swap") & reply_to_my_list_message_filter)
        async def swap_by_index(_, message: Message):
            first, second = get_two_indexes_from_parameters(message.text)
            record_dict, header = get_order_record_dict_and_header(message.reply_to_message.text)
            record_dict: OrderedDict = swap_records_by_indexes(first, second, record_dict)
            await self.__edit_student_queue(record_dict, header, incoming_message=message)

        @on_typed_message(self, filters.command("header") & reply_to_my_list_message_filter)
        async def set_header(_, message: Message):
            new_header: str = SCROLL_EMOJI + ' ' + get_single_text_parameter(message.text)
            record_dict, _ = get_order_record_dict_and_header(message.reply_to_message.text)
            await self.__edit_student_queue(record_dict, header=new_header, incoming_message=message)

        @on_typed_message(self, filters.command("queue"))
        async def create_queue(_, message: Message):
            header: str = get_single_text_parameter(message.text, should_exist=False)
            header = SCROLL_EMOJI + ' ' + header
            message = await self.send_reply_message(message, header, reply_markup=self.__help_markup)
            await message.pin(both_sides=True)

        @self.on_callback_query(filters.regex(r"^" + HELP_TITLE))
        async def show_helpful_alert(_, callback_query: CallbackQuery):
            helpful_message: str = callback_query.data[len(HELP_TITLE):]
            await callback_query.answer(helpful_message, show_alert=True)

        @on_typed_message(self, reply_to_my_list_message_filter)
        async def add_to_queue(_, message: Message):
            record_index, record_value = create_record(message.text)
            record_dict, header = get_order_record_dict_and_header(message.reply_to_message.text)

            if len(record_dict) >= 256:
                raise TelegramBotException("Queue is full. 256 records is maximum")

            # if queue is empty
            if len(record_dict) == 0:
                return await self.__edit_student_queue(OrderedDict({1: record_value}), header, incoming_message=message)

            # if no index
            if record_index is None:
                record_index: int = list(record_dict.keys())[-1] + 1
                record_dict[record_index] = record_value
                return await self.__edit_student_queue(record_dict, header, incoming_message=message)

            # if index is occupied
            if record_index in record_dict.keys():
                raise TelegramBotException("Index is occupied")

            record_dict[record_index] = record_value
            return await self.__edit_student_queue(record_dict, header, incoming_message=message)
