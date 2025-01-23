from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any

from griff.appli.event.event import Event, EventName
from griff.appli.message.message_handler import MessageHandler
from griff.infra.registry.meta_registry import (
    MetaEventHandlerRegistry,
)

E = TypeVar("E", bound=Event)


class EventHandler(
    Generic[E], MessageHandler[E, None], ABC, metaclass=MetaEventHandlerRegistry
):
    @abstractmethod
    async def handle(self, event: E) -> None:  # pragma: no cover
        pass

    @classmethod
    @abstractmethod
    def listen_to(cls) -> EventName:  # pragma: no cover
        pass


class FakeEventHandler(EventHandler, ABC):
    on_event_type: Type[Event]

    def __init__(self):
        super().__init__()
        self._log = {}

    async def handle(self, message: Event) -> None:
        self._log[message.event_name] = message.model_dump()  # type: ignore

    def list_events_handled(self) -> dict[str, Any]:
        return self._log

    @classmethod
    def listen_to(cls) -> EventName:
        return cls.on_event_type.message_name()
