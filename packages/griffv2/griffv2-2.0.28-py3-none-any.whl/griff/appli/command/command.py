from abc import ABC

from griff.appli.message.message import Message, MessageName

CommandName = MessageName


class Command(Message, ABC): ...
