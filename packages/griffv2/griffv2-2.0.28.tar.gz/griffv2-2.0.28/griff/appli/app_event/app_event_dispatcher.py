from griff.appli.app_event.app_event import AppEvent
from griff.appli.event.event import Event
from griff.appli.event.event_dispatcher import EventDispatcher
from griff.appli.message.message_middleware import MessageContext


class AppEventDispatcher(EventDispatcher[AppEvent, None]):

    async def dispatch(
        self, message: Event, context: MessageContext | None = None
    ) -> None:
        if isinstance(message, AppEvent) is False:
            raise RuntimeError(
                f"Event '{message.short_classname()}' must implement "
                "AppEventBusBroadcastable"
            )
        return await super().dispatch(message, context)
