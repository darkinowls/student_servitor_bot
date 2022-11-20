import unittest

from pymongo.collection import Collection
from pymongo.database import Database

from bot.database._connection import get_gmail_sessions
from bot.email import get_new_messages


class MyTestCase(unittest.TestCase):

    def test_database(self):
        gmail_s: Collection = get_gmail_sessions()
        doc = gmail_s.find_one({"chat_id": 16476882666})
        self.assertEqual("abobus@gmail.com", doc["email_address"])

    def test_unicode_escape(self):
        utf16_message = '\\u0414\\u043e\\u0431\\u0440\\u043e\\u0433\\u043e \\u0432\\u0435\\u0447\\u0435\\u0440\\u0430'
        text = utf16_message.encode().decode("unicode_escape")
        print(text)
        self.assertEqual("Доброго вечера", text)


if __name__ == '__main__':
    unittest.main()
