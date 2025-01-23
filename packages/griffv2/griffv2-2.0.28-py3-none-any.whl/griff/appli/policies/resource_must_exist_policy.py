from abc import ABC
from gettext import gettext as _
from typing import Generic, TypeVar

from griff.appli.policies.policy import PolicyException, CommonPolicy
from griff.domain.common_types import Entity
from griff.utils.errors import NotFoundError
from griff.utils.exceptions import EntityNotFoundException

E = TypeVar("E", bound=Entity)


class ResourceDoesNotExistError(NotFoundError): ...


class ResourceMustExistPolicy(Generic[E], CommonPolicy, ABC):
    async def check(self, resource_id: str) -> E:
        self.check_persistence()
        try:
            return await self.get_repository().get_by_id(resource_id)
        except EntityNotFoundException:
            message = _("'%(ressource)s' '%(id)s' does not exist") % {
                "id": resource_id,
                "ressource": self.get_ressource_name(),
            }
            raise PolicyException(ResourceDoesNotExistError(message=message))
