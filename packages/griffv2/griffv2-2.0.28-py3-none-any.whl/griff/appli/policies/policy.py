from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

from griff.infra.repository.repository import Repository
from griff.utils.errors import BaseError

E = TypeVar("E", bound=BaseError)


class PolicyException(Generic[E], Exception):
    def __init__(self, error: E) -> None:
        self.error = error


class Policy(ABC):
    async def check(self, *args, **kwargs) -> Any: ...


class CommonPolicy(Policy, ABC):
    def __init__(self):
        self.repository = None

    @abstractmethod
    def get_ressource_name(self) -> str:  # pragma: no cover
        ...

    @abstractmethod
    def get_repository(self) -> Repository:  # pragma: no cover
        ...

    def check_persistence(self) -> None:  # pragma: no cover
        if self.repository is None:
            raise ValueError(
                "repository not defined, you should call set a class "
                "attribute 'repository' with a value of type Repository"
            )
