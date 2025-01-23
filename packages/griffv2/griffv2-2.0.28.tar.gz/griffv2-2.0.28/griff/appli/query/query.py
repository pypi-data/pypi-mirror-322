from abc import ABC
from typing import Any

from griff.appli.message.message import Message, MessageName

QueryName = MessageName


class Query(Message, ABC):
    payload: Any

    @classmethod
    def message_name(cls) -> QueryName:
        return super().message_name()
