from abc import ABC
from gettext import gettext as _

from griff.appli.policies.policy import PolicyException, CommonPolicy
from griff.utils.errors import ConflictError
from griff.utils.exceptions import EntityNotFoundException


class ResourceAlreadyExistsError(ConflictError): ...


class ResourceMustNotExistPolicy(CommonPolicy, ABC):
    async def check(self, resource_id: str) -> None:
        self.check_persistence()
        try:
            await self.get_repository().get_by_id(resource_id)
            message = _("'%(ressource)s' '%(id)s' already exists") % {
                "id": resource_id,
                "ressource": self.get_ressource_name(),
            }
            raise PolicyException(ResourceAlreadyExistsError(message=message))
        except EntityNotFoundException:
            return None
