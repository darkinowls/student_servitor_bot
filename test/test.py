import unittest

from bot.helpers.datetime_helper import get_current_week_number, get_current_time_str, get_current_day_str


class MyTestCase(unittest.TestCase):

    def test_unicode_escape(self):
        utf16_message = '\\u0414\\u043e\\u0431\\u0440\\u043e\\u0433\\u043e \\u0432\\u0435\\u0447\\u0435\\u0440\\u0430'
        text = utf16_message.encode().decode("unicode_escape")
        print(text)
        self.assertEqual("Доброго вечера", text)

    def test_get_current_datetime(self):
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()
        print(week_num, day_str, time_str)

if __name__ == '__main__':
    unittest.main()
