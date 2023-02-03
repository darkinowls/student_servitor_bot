from abc import abstractmethod

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.database import Database

from bot.constants.load_env import MONGO_CONNECTION_STRING


class Session:

    def _get_database(self) -> Database:
        return MongoClient(MONGO_CONNECTION_STRING).get_database()

    @abstractmethod
    def __get_session_collection(self) -> Collection:
        pass

    @abstractmethod
    def set_session_module_is_on(self, chat_id: int, module_is_on: bool) -> bool:
        pass

    @abstractmethod
    def upsert_session(self, chat_id: int, session_data: list, module_is_on: bool = True) -> bool:
        pass

    @abstractmethod
    def get_all_sessions(self) -> Cursor:
        pass

    @abstractmethod
    def get_session_and_module_is_on_by_chat_id(self, chat_id: int) -> tuple[str | None, bool | None]:
        pass
