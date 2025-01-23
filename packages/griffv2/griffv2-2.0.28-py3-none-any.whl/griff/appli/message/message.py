from abc import ABC

from pydantic import BaseModel, ConfigDict

MessageName = str


class Message(BaseModel, ABC):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def classname(cls) -> str:
        return str(cls)

    @classmethod
    def short_classname(cls) -> str:
        return cls.__name__

    @classmethod
    def message_name(cls) -> MessageName:
        return cls.classname()
