from pymongo.collection import Collection
from pymongo.cursor import Cursor

from bot.constants.database import SCHEDULE_SESSIONS, CHAT_ID, SET_COMMAND, MODULE_IS_ON, SCHEDULE, ID
from bot.database.session import Session


class ScheduleSession(Session):

    def __get_session_collection(self) -> Collection:
        return self._get_database().get_collection(SCHEDULE_SESSIONS)

    def set_session_module_is_on(self, chat_id: int, module_is_on: bool) -> bool:
        return self.__get_session_collection().update_one({CHAT_ID: chat_id},
                                                                    {SET_COMMAND: {
                                                                        MODULE_IS_ON: module_is_on}}).matched_count == 1

    def upsert_session(self, chat_id: int, schedule: list[dict], module_is_on: bool = True) -> bool:
        return self.__get_session_collection().update_one({CHAT_ID: chat_id},
                                                               {SET_COMMAND: {
                                                                   SCHEDULE: schedule,
                                                                   MODULE_IS_ON: module_is_on
                                                               }},
                                                               upsert=True).matched_count == 1

    def get_session_and_module_is_on_by_chat_id(self, chat_id: int) -> tuple[str | None, bool | None]:
        result: dict = self.__get_session_collection().find_one(
            {CHAT_ID: chat_id},
            {SCHEDULE: 1, MODULE_IS_ON: 1, ID: 0}
        )
        if result is None:
            return None, None
        return result.get(SCHEDULE), result.get(MODULE_IS_ON)

    def get_all_sessions(self) -> Cursor:
        return self.__get_session_collection().find()