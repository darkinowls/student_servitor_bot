from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from bot.core.singleton_meta import SingletonMeta


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
