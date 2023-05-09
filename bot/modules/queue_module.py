from collections import OrderedDict

from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.filters import Filter
from pyrogram.types import CallbackQuery

from bot.constants.commands import RM, HEADER, QUEUE, Q
from bot.constants.general import WHITESPACE
from bot.constants.help_alerts import HELP_TITLE
from bot.constants.regex import SWAP_REGEX
from bot.decorators.on_message import on_message
from bot.exceptions.telegram_bot_warning import TelegramBotWarning
from bot.helpers.parameter_helper import get_single_text_parameter
from bot.helpers.queue_helper import Message, \
    get_order_record_dict_and_header_from_queue, \
    format_to_text, SCROLL_EMOJI, check_reply_to_my_queue_message, \
    swap_records_by_indexes, remove_records_by_indexes, create_queue_help_markup, \
    add_record_to_record_dict
from bot.helpers.record_helper import get_index_list_from_parameters, get_two_unique_indexes_from_parameters, \
    create_record
from bot.modules.simple_client import SimpleClient


class QueueModule(SimpleClient):

    async def __edit_student_queue(self, record_dict: OrderedDict, header: str, incoming_message: Message):
        queue_text: str = format_to_text(record_dict, header)
        await self.edit_replied_message(incoming_message, queue_text, reply_markup=self.__help_markup)

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        reply_to_my_list_message_filter: Filter = filters.create(check_reply_to_my_queue_message)
        self.__help_markup = create_queue_help_markup()

        @on_message(self, filters.command(RM))
        async def remove_by_indexes(_, message: Message):
            await check_reply_to_my_queue_message(_, self, message, raiseable=True)
            index_list: list[int] = get_index_list_from_parameters(message.text)
            record_dict, header = get_order_record_dict_and_header_from_queue(message.reply_to_message.text)
            record_dict: OrderedDict = remove_records_by_indexes(index_list, record_dict)
            await self.__edit_student_queue(record_dict, header, incoming_message=message)

        @on_message(self, reply_to_my_list_message_filter and filters.command('swap'))
        async def swap_by_index(_, message: Message):
            first, second = get_two_unique_indexes_from_parameters(message.text)
            record_dict, header = get_order_record_dict_and_header_from_queue(message.reply_to_message.text)
            record_dict: OrderedDict = swap_records_by_indexes(first, second, record_dict)
            await self.__edit_student_queue(record_dict, header, incoming_message=message)

        @on_message(self, filters.command(HEADER))
        async def set_header(_, message: Message):
            await check_reply_to_my_queue_message(_, self, message, raiseable=True)
            new_header: str = SCROLL_EMOJI + WHITESPACE + get_single_text_parameter(message.text)
            record_dict, _ = get_order_record_dict_and_header_from_queue(message.reply_to_message.text)
            await self.__edit_student_queue(record_dict, header=new_header, incoming_message=message)

        @on_message(self, filters.command([QUEUE, Q]))
        async def create_queue(_, message: Message):
            header: str = get_single_text_parameter(message.text, should_exist=False)
            header = SCROLL_EMOJI + WHITESPACE + header
            message = await self.send_reply_message(message, header, reply_markup=self.__help_markup)
            try:
                await message.pin(both_sides=True)
            except RPCError:
                raise TelegramBotWarning("Додайте боту право прикріплювати повідомлення в чаті")

        @self.on_callback_query(filters.regex(r"^" + HELP_TITLE))
        async def show_helpful_alert(_, callback_query: CallbackQuery):
            helpful_message: str = callback_query.data[len(HELP_TITLE):]
            await callback_query.answer(helpful_message, show_alert=True)

        @on_message(self, reply_to_my_list_message_filter)
        async def add_to_queue(_, message: Message):
            record_index, record_value = create_record(message.text)
            record_dict, header = get_order_record_dict_and_header_from_queue(message.reply_to_message.text)
            record_dict = add_record_to_record_dict(record_dict, record_index, record_value)
            return await self.__edit_student_queue(record_dict, header, incoming_message=message)
