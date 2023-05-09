HELP_TITLE = "H"

SWAP_HELP = HELP_TITLE + "/swap 1 2\n" \
                         "Swaps the replied queue records by indexes"

RM_HELP = HELP_TITLE + "/rm 1 2 .. 5\n" \
                       "Deletes the replied queue records by indexes"

HEADER_HELP = HELP_TITLE + "/header Lab 5 Math\n" \
                           "Sets the replied queue header"

ADD_HELP = HELP_TITLE + "Reply the queue and enter your name with index or not"

ALL_COMMANDS = \
    """
Команди:
    
/queue або /q - Створює чергу

/gmail [gmail] [app-pass] - Створює з’єднання між цим чатом та gmail                       

/gmail - Надсилає адресу gmail, яку встановив користувач

/schedule [file.json] - Бере файл формату json і встановлює розклад для групи

/schedule - Повертає файл json, встановлений користувачем. Якщо його немає, надсилається приклад json          

/hi - Відповідає привіт

/week - Повідомляє номер поточного тижня

/help - Надсилає повідомлення з усіма командами
    """

# LABELS

HOW_TO_ADD = "Як додавати запис?"

HOW_TO_SET_HEADER = "Як встановити заголовок?"

HOW_TO_REMOVE = "Як видаляти запис?"

HOW_TO_SWAP = "Як переміщувати запиcи?"
