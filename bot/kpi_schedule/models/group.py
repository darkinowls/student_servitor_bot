from dataclasses import dataclass
from typing import Any


@dataclass
class Group:
    id: str
    name: str
    faculty: str

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _faculty = str(obj.get("faculty"))
        return Group(_id, _name, _faculty)