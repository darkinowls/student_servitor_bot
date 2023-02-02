from unittest import TestCase

from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.queue_helper import get_index_list_from_parameters

NUM_LIST = [1, 2, 3, 4, 5]


class Test(TestCase):

    def test_get_index_list_from_parameters1(self):
        param_text: str = "/rm 1 2 3 4 5"
        i_list: list[int] = get_index_list_from_parameters(param_text)
        self.assertEqual(NUM_LIST, i_list)

        param_text: str = "/rm 1 .. 4 5"
        i_list: list[int] = get_index_list_from_parameters(param_text)
        self.assertEqual(NUM_LIST, i_list)

        param_text: str = "/rm 1 ..5"
        self.assertRaises(TelegramBotError,
                          get_index_list_from_parameters, param_text)

    def test_get_index_list_from_parameters2(self):
        param_text: str = "/rm 1 .. 3 .. 5"
        i_list: list[int] = get_index_list_from_parameters(param_text)
        self.assertEqual(NUM_LIST, i_list )

        param_text: str = "/rm 1 .. 4 .. 5"
        i_list: list[int] = get_index_list_from_parameters(param_text)
        self.assertEqual(NUM_LIST, i_list)

        param_text: str = "/rm 1 .."
        self.assertRaises(TelegramBotError,
                          get_index_list_from_parameters, param_text)
