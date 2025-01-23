from abc import ABC
from typing import Any, Optional

from pydantic import Field, model_validator

from griff.appli.message.message import Message, MessageName
from griff.services.date.date_models import DateTime
from griff.services.date.date_service import DateService
from griff.services.service_locator.service_locator import ServiceLocator
from griff.services.uniqid.uniqid_service import UniqIdService

EventName = MessageName


class Event(Message, ABC):
    id: str = Field(
        default_factory=lambda: ServiceLocator.get(UniqIdService).get("event")
    )
    payload: Any
    created_at: DateTime = Field(
        default_factory=lambda: ServiceLocator.get(DateService).now()
    )
    event_name: Optional[EventName] = None

    @model_validator(mode="before")
    def set_event_name(cls, data: Any) -> Any:
        data["event_name"] = cls.message_name()
        return data

    @classmethod
    def message_name(cls) -> EventName:
        return cls.short_classname()
