import unittest


class MyTestCase(unittest.TestCase):

    def test_unicode_escape(self):
        utf16_message = '\\u0414\\u043e\\u0431\\u0440\\u043e\\u0433\\u043e \\u0432\\u0435\\u0447\\u0435\\u0440\\u0430'
        text = utf16_message.encode().decode("unicode_escape")
        print(text)
        self.assertEqual("Доброго вечера", text)


if __name__ == '__main__':
    unittest.main()
