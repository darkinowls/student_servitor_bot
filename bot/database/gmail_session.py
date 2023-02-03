from pymongo.collection import Collection
from pymongo.cursor import Cursor

from bot.constants.database import GMAIL_SESSIONS, CHAT_ID, SET_COMMAND, MODULE_IS_ON, GMAIL_ADDRESS, APP_PASSWORD, ID
from bot.database.session import Session


class GmailSession(Session):

    def __get_session_collection(self) -> Collection:
        return self._get_database().get_collection(GMAIL_SESSIONS)

    def set_session_module_is_on(self, chat_id: int, module_is_on: bool) -> bool:
        return self.__get_session_collection().update_one({CHAT_ID: chat_id},
                                                          {SET_COMMAND: {
                                                              MODULE_IS_ON: module_is_on}}).matched_count == 1

    def upsert_session(self, chat_id: int, session_data: list[str], module_is_on: bool = True) -> bool:
        gmail_address: str = session_data[0]
        app_password: str = session_data[0]
        return self.__get_session_collection().update_one({CHAT_ID: chat_id},
                                                          {SET_COMMAND: {
                                                              GMAIL_ADDRESS: gmail_address,
                                                              APP_PASSWORD: app_password,
                                                              MODULE_IS_ON: module_is_on
                                                          }},
                                                          upsert=True).matched_count == 1

    def get_session_and_module_is_on_by_chat_id(self, chat_id: int) -> tuple[str | None, bool | None]:
        result: dict = self.__get_session_collection().find_one(
            {CHAT_ID: chat_id},
            {GMAIL_ADDRESS: 1, MODULE_IS_ON: 1, ID: 0}
        )
        if result is None:
            return None, None
        return result.get(GMAIL_ADDRESS), result.get(MODULE_IS_ON)

    def get_all_sessions(self) -> Cursor:
        return self.__get_session_collection().find()