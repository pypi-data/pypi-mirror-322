from abc import ABC, abstractmethod
from typing import Type, TypeVar

from loguru import logger
from pydantic import ValidationError

from griff.appli.app_event.app_event import AppEvent, AppEventName
from griff.appli.message.message_handler import MessageHandler
from griff.domain.common_types import Entity, DTO
from griff.infra.registry.meta_registry import MetaAppEventHandlerRegistry

E = TypeVar("E", Entity, DTO)


class AppEventHandler(
    MessageHandler[AppEvent, None], ABC, metaclass=MetaAppEventHandlerRegistry
):
    @abstractmethod
    async def handle(self, event: AppEvent) -> None:  # pragma: no cover
        pass

    @classmethod
    @abstractmethod
    def listen_to(cls) -> AppEventName:  # pragma: no cover
        pass

    @staticmethod
    def check_event_payload(event: AppEvent, valid_class: Type[E]) -> E | None:
        try:
            return valid_class(**event.payload)
        except ValidationError as e:
            logger.error(f"Erreur de validation {valid_class.short_classname()}: {e}")
            return None
