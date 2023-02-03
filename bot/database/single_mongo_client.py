from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SingleMongoClient(metaclass=SingletonMeta):
    __mongo_client: MongoClient

    def __init__(self, connection_string: str):
        self.__mongo_client = MongoClient(connection_string)
        try:
            self.__mongo_client.admin.command('ping')
        except ConnectionFailure:
            print("Server not available. Change MONGO_CONNECTION_STRING in the .env file")

    def get_database(self):
        return self.__mongo_client.get_database()
