from typing import Any

from pydantic import model_validator, BaseModel

from griff.appli.event.event import Event, EventName
from griff.appli.message.message import MessageName

AppEventName = MessageName


class AppEvent(Event):
    event_name: EventName

    @model_validator(mode="before")
    def set_event_name(cls, data: Any) -> Any:
        if isinstance(data["payload"], BaseModel):  # pragma: no cover
            # to avoid creation mistake in test unit
            raise RuntimeError("payload should not be a Pydantic model")
        data["event_name"] = data["event_name"]
        return data


class AppEventBusBroadcastable(Event):
    def to_app_event(self) -> AppEvent:
        return AppEvent(**self.model_dump())
